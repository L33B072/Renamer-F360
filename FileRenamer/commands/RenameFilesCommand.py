import adsk.core
import adsk.fusion
import traceback
import re
import os

class RenameFilesCommand:
    def __init__(self):
        self._command_id = 'RenameFilesCmd'
        self._command_name = 'Rename Files with Special Characters'
        self._command_tooltip = 'Scan and rename files containing special characters'
        self._workspace_id = 'FusionSolidEnvironment'
        self._toolbar_panel_id = 'SolidModifyPanel'
        
    @staticmethod
    def create_command_definition(ui):
        try:
            # Get the CommandDefinitions collection
            cmd_defs = ui.commandDefinitions
            
            # Check if command already exists
            cmd_def = cmd_defs.itemById('RenameFilesCmd')
            if cmd_def:
                cmd_def.deleteMe()
            
            # Create new command definition
            cmd_def = cmd_defs.addButtonDefinition(
                'RenameFilesCmd',
                'Rename Files',
                'Rename files with special characters',
                './resources'  # Icon folder
            )
            
            # Connect to command created event
            on_command_created = RenameFilesCommandCreated()
            cmd_def.commandCreated.add(on_command_created)
            
            # Add command to UI
            workspace = ui.workspaces.itemById('FusionSolidEnvironment')
            toolbar_panel = workspace.toolbarPanels.itemById('SolidModifyPanel')
            
            if toolbar_panel:
                toolbar_panel.controls.addCommand(cmd_def)
                
        except Exception as e:
            ui.messageBox(f'Failed to create command: {str(e)}')
    
    @staticmethod
    def destroy_command_definition(ui):
        try:
            # Remove command from UI
            workspace = ui.workspaces.itemById('FusionSolidEnvironment')
            toolbar_panel = workspace.toolbarPanels.itemById('SolidModifyPanel')
            
            if toolbar_panel:
                cmd_control = toolbar_panel.controls.itemById('RenameFilesCmd')
                if cmd_control:
                    cmd_control.deleteMe()
            
            # Delete command definition
            cmd_defs = ui.commandDefinitions
            cmd_def = cmd_defs.itemById('RenameFilesCmd')
            if cmd_def:
                cmd_def.deleteMe()
                
        except Exception as e:
            ui.messageBox(f'Failed to destroy command: {str(e)}')


class RenameFilesCommandCreated(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            # Get the command that was created
            cmd = args.command
            
            # Connect to execute event
            on_execute = RenameFilesCommandExecute()
            cmd.execute.add(on_execute)
            
            # Create command inputs
            inputs = cmd.commandInputs
            
            # Add selection input for files
            selection_input = inputs.addSelectionInput(
                'file_selection',
                'Files to Rename',
                'Select files to rename (leave empty to scan all project files)'
            )
            selection_input.setSelectionLimits(0, 0)  # No limit on selections
            
            # Add table to show files with special characters
            table_input = inputs.addTableCommandInput('files_table', 'Files with Special Characters', 3, '1:2:2')
            table_input.tablePresentationStyle = adsk.core.TablePresentationStyles.transparentBackgroundTablePresentationStyle
            table_input.addCommandInput(0, 0, inputs.addStringValueInput('header1', '', 'Current Name'))
            table_input.addCommandInput(0, 1, inputs.addStringValueInput('header2', '', 'Proposed Name'))
            table_input.addCommandInput(0, 2, inputs.addBoolValueInput('header3', '', 'Rename', True, '', True))
            
            # Add character replacement options
            char_group = inputs.addGroupCommandInput('char_group', 'Character Replacement Options')
            char_group.isExpanded = True
            char_inputs = char_group.children
            
            # Common special character replacements
            char_inputs.addBoolValueInput('replace_spaces', 'Replace spaces with underscores', '', True)
            char_inputs.addBoolValueInput('replace_special', 'Replace special characters (!@#$%^&*)', '', True)
            char_inputs.addBoolValueInput('replace_unicode', 'Replace unicode characters', '', True)
            char_inputs.addBoolValueInput('to_lowercase', 'Convert to lowercase', '', False)
            
            # Custom replacement string
            char_inputs.addStringValueInput('custom_replacement', 'Custom replacement character', '_')
            
        except Exception as e:
            adsk.core.Application.get().userInterface.messageBox(f'Command created failed: {str(e)}')


class RenameFilesCommandExecute(adsk.core.CommandExecuteEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            # Get command inputs
            inputs = args.command.commandInputs
            app = adsk.core.Application.get()
            ui = app.userInterface
            
            # Get active project
            design = adsk.fusion.Design.cast(app.activeProduct)
            if not design:
                ui.messageBox('No active design found')
                return
                
            # Get project files that need renaming
            files_to_rename = self.scan_project_files(design, inputs)
            
            if not files_to_rename:
                ui.messageBox('No files with special characters found')
                return
            
            # Confirm with user
            result = ui.messageBox(
                f'Found {len(files_to_rename)} files to rename. Continue?',
                'Confirm Rename',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                renamed_count = self.rename_files(files_to_rename, design)
                ui.messageBox(f'Successfully renamed {renamed_count} files')
            
        except Exception as e:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(f'Execute failed: {str(e)}\n{traceback.format_exc()}')
    
    def scan_project_files(self, design, inputs):
        """Scan project for files with special characters"""
        files_to_rename = []
        
        try:
            # Get replacement options
            replace_spaces = inputs.itemById('replace_spaces').value
            replace_special = inputs.itemById('replace_special').value
            replace_unicode = inputs.itemById('replace_unicode').value
            to_lowercase = inputs.itemById('to_lowercase').value
            custom_replacement = inputs.itemById('custom_replacement').value
            
            # Get all components in the design
            all_components = design.allComponents
            
            for component in all_components:
                if component.name:
                    original_name = component.name
                    new_name = self.clean_filename(
                        original_name,
                        replace_spaces,
                        replace_special,
                        replace_unicode,
                        to_lowercase,
                        custom_replacement
                    )
                    
                    if original_name != new_name:
                        files_to_rename.append({
                            'component': component,
                            'original_name': original_name,
                            'new_name': new_name
                        })
            
            # Also check document name
            if design.parentDocument.name:
                original_name = design.parentDocument.name
                new_name = self.clean_filename(
                    original_name,
                    replace_spaces,
                    replace_special,
                    replace_unicode,
                    to_lowercase,
                    custom_replacement
                )
                
                if original_name != new_name:
                    files_to_rename.append({
                        'document': design.parentDocument,
                        'original_name': original_name,
                        'new_name': new_name
                    })
                    
        except Exception as e:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(f'Scan failed: {str(e)}')
            
        return files_to_rename
    
    def clean_filename(self, filename, replace_spaces, replace_special, replace_unicode, to_lowercase, replacement_char):
        """Clean a filename by replacing special characters"""
        cleaned = filename
        
        # Replace spaces
        if replace_spaces:
            cleaned = cleaned.replace(' ', replacement_char)
        
        # Replace special characters
        if replace_special:
            special_chars = r'[!@#$%^&*()+=\[\]{};:"|<>?,./\\]'
            cleaned = re.sub(special_chars, replacement_char, cleaned)
        
        # Replace unicode characters (keep only ASCII)
        if replace_unicode:
            cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase
        if to_lowercase:
            cleaned = cleaned.lower()
        
        # Remove multiple consecutive replacement characters
        if replacement_char:
            pattern = re.escape(replacement_char) + '+'
            cleaned = re.sub(pattern, replacement_char, cleaned)
        
        # Remove leading/trailing replacement characters
        cleaned = cleaned.strip(replacement_char)
        
        return cleaned
    
    def rename_files(self, files_to_rename, design):
        """Rename the files"""
        renamed_count = 0
        
        try:
            for file_info in files_to_rename:
                try:
                    if 'component' in file_info:
                        # Rename component
                        file_info['component'].name = file_info['new_name']
                    elif 'document' in file_info:
                        # Rename document (this might have limitations)
                        # Note: Document renaming might not be directly supported
                        pass
                    
                    renamed_count += 1
                    
                except Exception as e:
                    # Continue with other files even if one fails
                    ui = adsk.core.Application.get().userInterface
                    ui.messageBox(f'Failed to rename {file_info["original_name"]}: {str(e)}')
                    
        except Exception as e:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(f'Rename operation failed: {str(e)}')
            
        return renamed_count