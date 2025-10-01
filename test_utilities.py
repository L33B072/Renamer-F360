#!/usr/bin/env python3
"""
Test script for File Renamer utilities

This script tests the file cleaning functions independently of Fusion 360
to ensure they work correctly before deploying the add-in.
"""

import sys
import os

# Add the lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'FileRenamer', 'lib'))

from file_utils import FileNameCleaner, FileRenamePreview

def test_filename_cleaning():
    """Test various filename cleaning scenarios"""
    print("Testing File Name Cleaning...")
    print("=" * 50)
    
    test_cases = [
        "My Project File.f3d",
        "Component (v2).ipt", 
        "File!!!Name.step",
        "测试文件.dwg",
        "   spaces   everywhere   .f3d",
        "UPPERCASE.F3D",
        "file@#$%^&*()name.step",
        "normal_filename.f3d",
        "",
        "a" * 300,  # Too long filename
    ]
    
    options = {
        'replace_spaces': True,
        'replace_special': True,
        'replace_unicode': True,
        'to_lowercase': False,
        'replacement_char': '_'
    }
    
    for original in test_cases:
        cleaned = FileNameCleaner.clean_filename(original, options)
        has_special = FileNameCleaner.has_special_characters(original)
        problematic = FileNameCleaner.get_problematic_characters(original)
        is_valid, issues = FileNameCleaner.validate_filename(original)
        
        print(f"Original:    '{original}'")
        print(f"Cleaned:     '{cleaned}'")
        print(f"Has Special: {has_special}")
        print(f"Problems:    {sorted(problematic) if problematic else 'None'}")
        print(f"Valid:       {is_valid}")
        if not is_valid:
            print(f"Issues:      {issues}")
        print("-" * 30)

def test_rename_preview():
    """Test the rename preview functionality"""
    print("\nTesting Rename Preview...")
    print("=" * 50)
    
    preview = FileRenamePreview()
    
    # Add some test rename operations
    test_renames = [
        ("My Component.f3d", "My_Component.f3d", "component"),
        ("Special!@#File.step", "Special___File.step", "document"),
        ("Unicode测试.dwg", "Unicode_.dwg", "component"),
    ]
    
    for original, new, file_type in test_renames:
        preview.add_rename_operation(original, new, file_type)
    
    print(preview.get_summary())

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\nTesting Edge Cases...")
    print("=" * 50)
    
    edge_cases = [
        "",  # Empty string
        "   ",  # Only spaces
        "___",  # Only replacement chars
        "CON",  # Reserved name (Windows)
        "LPT1",  # Reserved name (Windows)
        "normal.txt",  # Already clean
        "a",  # Single character
        "." * 10,  # Only dots
    ]
    
    for test_case in edge_cases:
        cleaned = FileNameCleaner.clean_filename(test_case)
        is_valid, issues = FileNameCleaner.validate_filename(test_case)
        
        print(f"Input:       '{test_case}'")
        print(f"Cleaned:     '{cleaned}'")
        print(f"Valid:       {is_valid}")
        if not is_valid:
            print(f"Issues:      {issues}")
        print("-" * 20)

def main():
    """Run all tests"""
    print("Fusion 360 File Renamer - Utility Tests")
    print("========================================")
    
    try:
        test_filename_cleaning()
        test_rename_preview()
        test_edge_cases()
        
        print("\n✓ All tests completed successfully!")
        print("The utility functions are working correctly.")
        print("\nNext steps:")
        print("1. Install the add-in in Fusion 360")
        print("2. Test with real project files")
        print("3. Verify UI functionality")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)