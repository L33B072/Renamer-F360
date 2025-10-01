"""
File Renamer Utilities

This module contains utility functions for file name cleaning and validation.
"""

import re
import string

class FileNameCleaner:
    """Utility class for cleaning file names"""
    
    # Define common problematic characters
    SPECIAL_CHARS = r'[!@#$%^&*()+=\[\]{};:"|<>?,./\\`~]'
    UNICODE_CHARS = r'[^\x00-\x7F]'
    MULTIPLE_SPACES = r'\s+'
    MULTIPLE_UNDERSCORES = r'_+'
    
    @staticmethod
    def clean_filename(filename, options=None):
        """
        Clean a filename based on provided options
        
        Args:
            filename (str): Original filename
            options (dict): Cleaning options
                - replace_spaces: Replace spaces with underscores
                - replace_special: Replace special characters
                - replace_unicode: Replace unicode characters
                - to_lowercase: Convert to lowercase
                - replacement_char: Character to use for replacements
        
        Returns:
            str: Cleaned filename
        """
        if options is None:
            options = {
                'replace_spaces': True,
                'replace_special': True,
                'replace_unicode': True,
                'to_lowercase': False,
                'replacement_char': '_'
            }
        
        cleaned = filename
        replacement_char = options.get('replacement_char', '_')
        
        # Convert to lowercase first if requested
        if options.get('to_lowercase', False):
            cleaned = cleaned.lower()
        
        # Replace spaces
        if options.get('replace_spaces', True):
            cleaned = re.sub(FileNameCleaner.MULTIPLE_SPACES, replacement_char, cleaned)
        
        # Replace special characters
        if options.get('replace_special', True):
            cleaned = re.sub(FileNameCleaner.SPECIAL_CHARS, replacement_char, cleaned)
        
        # Replace unicode characters (keep only ASCII)
        if options.get('replace_unicode', True):
            cleaned = re.sub(FileNameCleaner.UNICODE_CHARS, replacement_char, cleaned)
        
        # Clean up multiple consecutive replacement characters
        if replacement_char:
            pattern = re.escape(replacement_char) + '+'
            cleaned = re.sub(pattern, replacement_char, cleaned)
        
        # Remove leading/trailing replacement characters
        cleaned = cleaned.strip(replacement_char)
        
        # Ensure we don't have an empty filename
        if not cleaned:
            cleaned = 'unnamed_file'
        
        return cleaned
    
    @staticmethod
    def has_special_characters(filename):
        """
        Check if filename contains special characters
        
        Args:
            filename (str): Filename to check
            
        Returns:
            bool: True if filename contains special characters
        """
        # Check for spaces, special characters, or unicode
        if re.search(r'\s', filename):
            return True
        if re.search(FileNameCleaner.SPECIAL_CHARS, filename):
            return True
        if re.search(FileNameCleaner.UNICODE_CHARS, filename):
            return True
        
        return False
    
    @staticmethod
    def get_problematic_characters(filename):
        """
        Get list of problematic characters in filename
        
        Args:
            filename (str): Filename to analyze
            
        Returns:
            set: Set of problematic characters found
        """
        problematic = set()
        
        # Find spaces
        if re.search(r'\s', filename):
            problematic.update(re.findall(r'\s', filename))
        
        # Find special characters
        special_matches = re.findall(FileNameCleaner.SPECIAL_CHARS, filename)
        problematic.update(special_matches)
        
        # Find unicode characters
        unicode_matches = re.findall(FileNameCleaner.UNICODE_CHARS, filename)
        problematic.update(unicode_matches)
        
        return problematic
    
    @staticmethod
    def validate_filename(filename):
        """
        Validate if filename is acceptable for most systems
        
        Args:
            filename (str): Filename to validate
            
        Returns:
            tuple: (is_valid, issues_list)
        """
        issues = []
        
        if not filename:
            issues.append("Filename is empty")
        
        if len(filename) > 255:
            issues.append("Filename is too long (>255 characters)")
        
        if FileNameCleaner.has_special_characters(filename):
            problematic = FileNameCleaner.get_problematic_characters(filename)
            issues.append(f"Contains problematic characters: {', '.join(sorted(problematic))}")
        
        # Check for reserved names (Windows)
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL'] + \
                        [f'COM{i}' for i in range(1, 10)] + \
                        [f'LPT{i}' for i in range(1, 10)]
        
        if filename.upper() in reserved_names:
            issues.append(f"'{filename}' is a reserved system name")
        
        return len(issues) == 0, issues


class FileRenamePreview:
    """Class for previewing file rename operations"""
    
    def __init__(self):
        self.rename_operations = []
    
    def add_rename_operation(self, original_name, new_name, file_type='component'):
        """Add a rename operation to preview"""
        self.rename_operations.append({
            'original': original_name,
            'new': new_name,
            'type': file_type,
            'changes': self._get_changes(original_name, new_name)
        })
    
    def _get_changes(self, original, new):
        """Get description of changes made"""
        changes = []
        
        if original != new:
            if ' ' in original and '_' in new:
                changes.append("Replaced spaces with underscores")
            
            problematic_orig = FileNameCleaner.get_problematic_characters(original)
            problematic_new = FileNameCleaner.get_problematic_characters(new)
            
            if problematic_orig and not problematic_new:
                changes.append("Removed special characters")
            
            if original.lower() == new and original != new:
                changes.append("Converted to lowercase")
        
        return changes
    
    def get_summary(self):
        """Get summary of all rename operations"""
        if not self.rename_operations:
            return "No files need renaming"
        
        summary = f"Found {len(self.rename_operations)} files to rename:\n\n"
        
        for i, op in enumerate(self.rename_operations, 1):
            summary += f"{i}. {op['original']} → {op['new']}\n"
            if op['changes']:
                summary += f"   Changes: {', '.join(op['changes'])}\n"
            summary += "\n"
        
        return summary
    
    def clear(self):
        """Clear all rename operations"""
        self.rename_operations.clear()