import adsk.core
import adsk.fusion
import traceback
import re

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        ui.messageBox('Advanced Cloud File Renamer is starting...')
        
        # Get current project
        current_doc = app.activeDocument
        if not current_doc or not current_doc.dataFile:
            ui.messageBox('Please open a document first so we can access the project.')
            return
        
        current_project = current_doc.dataFile.parentProject
        if not current_project:
            ui.messageBox('Could not access the current project.')
            return
        
        ui.messageBox(f'Found project: {current_project.name}\\n\\nScanning for files with special characters...')
        
        # Scan the project for files that need renaming (using default options)
        files_to_rename = scan_project_for_files(current_project)
        
        if not files_to_rename:
            ui.messageBox('No files with special characters found in this project.')
            return
        
        # Show individual file preview
        show_file_preview(ui, files_to_rename)
        
    except:
        if ui:
            ui.messageBox('Error in Advanced Cloud File Renamer:\n{}'.format(traceback.format_exc()))

def scan_project_for_files(project):
    """Scan project for files that need renaming"""
    files_to_rename = []
    
    try:
        # Get root folder of project
        root_folder = project.rootFolder
        scan_folder_recursive(root_folder, files_to_rename)
    except:
        pass
    
    return files_to_rename

def scan_folder_recursive(folder, files_to_rename):
    """Recursively scan folder for files"""
    try:
        # Scan files in current folder
        data_files = folder.dataFiles
        for i in range(data_files.count):
            data_file = data_files.item(i)
            
            original_name = data_file.name
            cleaned_name = clean_filename(original_name)
            
            if original_name != cleaned_name:
                folder_path = get_folder_path(folder)
                files_to_rename.append({
                    'data_file': data_file,
                    'original_name': original_name,
                    'new_name': cleaned_name,
                    'folder_path': folder_path
                })
        
        # Scan subfolders
        sub_folders = folder.dataFolders
        for i in range(sub_folders.count):
            sub_folder = sub_folders.item(i)
            scan_folder_recursive(sub_folder, files_to_rename)
    except:
        pass

def get_folder_path(folder):
    """Get the full path of a folder"""
    try:
        path_parts = []
        current_folder = folder
        
        while current_folder:
            path_parts.insert(0, current_folder.name)
            current_folder = current_folder.parentFolder
        
        return ' > '.join(path_parts)
    except:
        return 'Unknown Path'

def show_file_preview(ui, files_to_rename):
    """Show individual file preview and approval"""
    try:
        files_to_process = []
        skipped_count = 0
        
        for file_info in files_to_rename:
            original_name = file_info['original_name']
            new_name = file_info['new_name']
            folder_path = file_info['folder_path']
            
            # Highlight problematic characters
            display_original = original_name
            problematic_chars = ['"', "'", '/', '\\', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '[', ']', '{', '}', ';', ':', '|', '<', '>', '?', ',', '.', '`', '~', ' ']
            problem_chars_found = []
            
            for char in problematic_chars:
                if char in display_original:
                    if char == ' ':
                        problem_chars_found.append('SPACE')
                    else:
                        problem_chars_found.append(char)
                    display_original = display_original.replace(char, f'[{char}]')
            
            # Create preview message
            preview_msg = f'Location: {folder_path}\\n\\n'
            preview_msg += f'Current name: {display_original}\\n'
            preview_msg += f'New name: {new_name}\\n\\n'
            preview_msg += f'Problems found: {", ".join(problem_chars_found)}\\n\\n'
            preview_msg += f'Rename this file?\\n\\n'
            preview_msg += f'(File {len(files_to_process) + skipped_count + 1} of {len(files_to_rename)})'
            
            result = ui.messageBox(
                preview_msg,
                'Rename Cloud File?',
                adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                files_to_process.append(file_info)
            elif result == adsk.core.DialogResults.DialogNo:
                skipped_count += 1
            else:  # Cancel
                break
        
        # Confirm batch rename
        if files_to_process:
            summary_msg = f'Ready to rename {len(files_to_process)} cloud files'
            if skipped_count > 0:
                summary_msg += f' (skipped {skipped_count})'
            summary_msg += '\\n\\nProceed with batch rename?'
            
            final_result = ui.messageBox(
                summary_msg,
                'Confirm Cloud File Rename',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType
            )
            
            if final_result == adsk.core.DialogResults.DialogYes:
                perform_cloud_file_renames(ui, files_to_process)
            else:
                ui.messageBox('Rename operation cancelled')
        else:
            ui.messageBox('No files selected for renaming')
            
    except:
        ui.messageBox('Preview failed:\n{}'.format(traceback.format_exc()))

def perform_cloud_file_renames(ui, files_to_rename):
    """Perform the actual cloud file renames"""
    renamed_count = 0
    failed_files = []
    
    for file_info in files_to_rename:
        try:
            data_file = file_info['data_file']
            new_name = file_info['new_name']
            
            # Rename the cloud file
            data_file.name = new_name
            renamed_count += 1
            
        except Exception as e:
            failed_files.append(f"{file_info['original_name']}: {str(e)}")
    
    # Show results
    result_message = f'Successfully renamed {renamed_count} of {len(files_to_rename)} cloud files'
    
    if failed_files:
        result_message += f'\\n\\nFailed to rename {len(failed_files)} files:'
        for failure in failed_files[:5]:  # Show first 5 failures
            result_message += f'\\n- {failure}'
        if len(failed_files) > 5:
            result_message += f'\\n... and {len(failed_files) - 5} more'
    
    ui.messageBox(result_message)

def clean_filename(filename):
    """Clean a filename by replacing special characters"""
    cleaned = filename
    
    # Replace spaces
    cleaned = cleaned.replace(' ', '_')
    
    # Replace special characters (including quotes and slashes)
    special_chars = r'[!@#$%^&*()+=\[\]{};:"|<>?,./\\`~\'"]'
    cleaned = re.sub(special_chars, '_', cleaned)
    
    # Replace unicode characters (keep only ASCII)
    cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
    
    # Clean up multiple consecutive replacement characters
    cleaned = re.sub('_+', '_', cleaned)
    
    # Remove leading/trailing replacement characters
    cleaned = cleaned.strip('_')
    
    # Ensure we don't have an empty filename
    if not cleaned:
        cleaned = 'unnamed_file'
    
    return cleaned

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Remove command from UI
        design_workspace = ui.workspaces.itemById('FusionSolidEnvironment')
        if design_workspace:
            modify_panel = design_workspace.toolbarPanels.itemById('SolidModifyPanel')
            if modify_panel:
                cmd_control = modify_panel.controls.itemById('CloudFileRenamerCmd')
                if cmd_control:
                    cmd_control.deleteMe()
        
        # Delete command definition
        cmd_defs = ui.commandDefinitions
        cmd_def = cmd_defs.itemById('CloudFileRenamerCmd')
        if cmd_def:
            cmd_def.deleteMe()
            
    except:
        if ui:
            ui.messageBox('Failed to stop Cloud File Renamer:\n{}'.format(traceback.format_exc()))


class CloudFileRenamerCommandCreated(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            cmd = args.command
            
            # Connect to execute event
            on_execute = CloudFileRenamerCommandExecute()
            cmd.executed.add(on_execute)
            
            # Create command inputs
            inputs = cmd.commandInputs
            
            # Add scope selection
            scope_group = inputs.addGroupCommandInput('scope_group', 'Scan Scope')
            scope_group.isExpanded = True
            scope_inputs = scope_group.children
            
            scope_inputs.addBoolValueInput('scan_current_project', 'Current Project only', '', True)
            scope_inputs.addBoolValueInput('scan_all_projects', 'All accessible projects', '', False)
            scope_inputs.addBoolValueInput('scan_current_folder', 'Current folder and subfolders', '', False)
            
            # Add file type selection
            file_types_group = inputs.addGroupCommandInput('file_types', 'Include File Types')
            file_types_group.isExpanded = True
            file_types_inputs = file_types_group.children
            
            file_types_inputs.addBoolValueInput('include_designs', 'Fusion 360 Designs (.f3d)', '', True)
            file_types_inputs.addBoolValueInput('include_drawings', 'Fusion 360 Drawings (.f2d)', '', True)
            file_types_inputs.addBoolValueInput('include_simulations', 'Simulation Studies', '', True)
            file_types_inputs.addBoolValueInput('include_cad_files', 'Imported CAD files', '', True)
            file_types_inputs.addBoolValueInput('include_other', 'Other file types', '', False)
            
            # Add rename options
            options_group = inputs.addGroupCommandInput('options_group', 'Rename Options')
            options_group.isExpanded = True
            options_inputs = options_group.children
            
            options_inputs.addBoolValueInput('replace_spaces', 'Replace spaces with underscores', '', True)
            options_inputs.addBoolValueInput('replace_special', 'Replace special characters (!@#$%^&*)', '', True)
            options_inputs.addBoolValueInput('replace_unicode', 'Replace unicode characters', '', True)
            options_inputs.addBoolValueInput('to_lowercase', 'Convert to lowercase', '', False)
            options_inputs.addStringValueInput('replacement_char', 'Replacement character', '_')
            
        except:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox('Command created failed:\n{}'.format(traceback.format_exc()))


class CloudFileRenamerCommandExecute(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        ui = None
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            
            # Get command inputs
            inputs = args.command.commandInputs
            
            # Get scope options
            scan_current_project = inputs.itemById('scan_current_project').value
            scan_all_projects = inputs.itemById('scan_all_projects').value
            scan_current_folder = inputs.itemById('scan_current_folder').value
            
            # Get file type options
            include_designs = inputs.itemById('include_designs').value
            include_drawings = inputs.itemById('include_drawings').value
            include_simulations = inputs.itemById('include_simulations').value
            include_cad_files = inputs.itemById('include_cad_files').value
            include_other = inputs.itemById('include_other').value
            
            # Get rename options
            replace_spaces = inputs.itemById('replace_spaces').value
            replace_special = inputs.itemById('replace_special').value
            replace_unicode = inputs.itemById('replace_unicode').value
            to_lowercase = inputs.itemById('to_lowercase').value
            replacement_char = inputs.itemById('replacement_char').value
            
            # Scan for files in Fusion 360 cloud
            files_to_rename = self.scan_cloud_files(
                app, scan_current_project, scan_all_projects, scan_current_folder,
                include_designs, include_drawings, include_simulations, include_cad_files, include_other,
                replace_spaces, replace_special, replace_unicode, to_lowercase, replacement_char
            )
            
            if not files_to_rename:
                ui.messageBox('No files with special characters found in the selected scope.')
                return
            
            # Show preview
            ui.messageBox(f'Found {len(files_to_rename)} files to rename.\\n\\nStarting individual file review...')
            self.show_file_preview(ui, files_to_rename)
            
        except:
            if ui:
                ui.messageBox('Execute failed:\n{}'.format(traceback.format_exc()))
    
    def scan_cloud_files(self, app, scan_current_project, scan_all_projects, scan_current_folder,
                        include_designs, include_drawings, include_simulations, include_cad_files, include_other,
                        replace_spaces, replace_special, replace_unicode, to_lowercase, replacement_char):
        """Scan Fusion 360 cloud files for renaming"""
        files_to_rename = []
        
        try:
            # Get the data manager
            data_mgr = app.data
            
            if scan_current_project:
                # Get current project
                current_doc = app.activeDocument
                if current_doc and current_doc.dataFile:
                    current_project = current_doc.dataFile.parentProject
                    if current_project:
                        files_to_rename.extend(self.scan_project_files(
                            current_project, include_designs, include_drawings, include_simulations, 
                            include_cad_files, include_other, replace_spaces, replace_special, 
                            replace_unicode, to_lowercase, replacement_char
                        ))
            
            elif scan_all_projects:
                # Get all projects (this might be limited by permissions)
                hub = data_mgr.activeHub
                if hub:
                    projects = hub.dataProjects
                    for i in range(projects.count):
                        project = projects.item(i)
                        files_to_rename.extend(self.scan_project_files(
                            project, include_designs, include_drawings, include_simulations,
                            include_cad_files, include_other, replace_spaces, replace_special,
                            replace_unicode, to_lowercase, replacement_char
                        ))
            
            elif scan_current_folder:
                # Get current folder and scan recursively
                current_doc = app.activeDocument
                if current_doc and current_doc.dataFile:
                    current_folder = current_doc.dataFile.parentFolder
                    if current_folder:
                        files_to_rename.extend(self.scan_folder_recursive(
                            current_folder, include_designs, include_drawings, include_simulations,
                            include_cad_files, include_other, replace_spaces, replace_special,
                            replace_unicode, to_lowercase, replacement_char
                        ))
                        
        except Exception as e:
            # Return what we found so far
            pass
        
        return files_to_rename
    
    def scan_project_files(self, project, include_designs, include_drawings, include_simulations, 
                          include_cad_files, include_other, replace_spaces, replace_special, 
                          replace_unicode, to_lowercase, replacement_char):
        """Scan all files in a project"""
        files_to_rename = []
        
        try:
            # Get root folder of project
            root_folder = project.rootFolder
            files_to_rename.extend(self.scan_folder_recursive(
                root_folder, include_designs, include_drawings, include_simulations,
                include_cad_files, include_other, replace_spaces, replace_special,
                replace_unicode, to_lowercase, replacement_char
            ))
        except:
            pass
        
        return files_to_rename
    
    def scan_folder_recursive(self, folder, include_designs, include_drawings, include_simulations,
                             include_cad_files, include_other, replace_spaces, replace_special,
                             replace_unicode, to_lowercase, replacement_char):
        """Recursively scan a folder and its subfolders"""
        files_to_rename = []
        
        try:
            # Scan files in current folder
            data_files = folder.dataFiles
            for i in range(data_files.count):
                data_file = data_files.item(i)
                
                # Check if we should include this file type
                if self.should_include_file(data_file, include_designs, include_drawings, 
                                          include_simulations, include_cad_files, include_other):
                    
                    original_name = data_file.name
                    cleaned_name = self.clean_filename(
                        original_name, replace_spaces, replace_special,
                        replace_unicode, to_lowercase, replacement_char
                    )
                    
                    if original_name != cleaned_name:
                        files_to_rename.append({
                            'data_file': data_file,
                            'original_name': original_name,
                            'new_name': cleaned_name,
                            'folder_path': self.get_folder_path(folder),
                            'file_type': self.get_file_type_description(data_file)
                        })
            
            # Recursively scan subfolders
            sub_folders = folder.dataFolders
            for i in range(sub_folders.count):
                sub_folder = sub_folders.item(i)
                files_to_rename.extend(self.scan_folder_recursive(
                    sub_folder, include_designs, include_drawings, include_simulations,
                    include_cad_files, include_other, replace_spaces, replace_special,
                    replace_unicode, to_lowercase, replacement_char
                ))
                
        except:
            pass
        
        return files_to_rename
    
    def should_include_file(self, data_file, include_designs, include_drawings, include_simulations, include_cad_files, include_other):
        """Determine if a file should be included based on its type"""
        try:
            file_extension = data_file.fileExtension.lower()
            
            if include_designs and file_extension in ['.f3d', '.f3z']:
                return True
            if include_drawings and file_extension in ['.f2d']:
                return True
            if include_simulations and 'simulation' in data_file.name.lower():
                return True  
            if include_cad_files and file_extension in ['.step', '.stp', '.iges', '.igs', '.dwg', '.dxf', '.sat', '.x_t', '.x_b']:
                return True
            if include_other and file_extension not in ['.f3d', '.f3z', '.f2d']:
                return True
                
        except:
            if include_other:
                return True
        
        return False
    
    def get_folder_path(self, folder):
        """Get the full path of a folder"""
        try:
            path_parts = []
            current_folder = folder
            
            while current_folder:
                path_parts.insert(0, current_folder.name)
                current_folder = current_folder.parentFolder
            
            return ' > '.join(path_parts)
        except:
            return 'Unknown Path'
    
    def get_file_type_description(self, data_file):
        """Get a description of the file type"""
        try:
            extension = data_file.fileExtension.lower()
            if extension in ['.f3d', '.f3z']:
                return 'Fusion 360 Design'
            elif extension == '.f2d':
                return 'Fusion 360 Drawing'
            elif extension in ['.step', '.stp']:
                return 'STEP File'
            elif extension in ['.iges', '.igs']:
                return 'IGES File'
            elif extension in ['.dwg', '.dxf']:
                return 'AutoCAD File'
            else:
                return f'{extension.upper()} File'
        except:
            return 'Unknown File Type'
    
    def show_file_preview(self, ui, files_to_rename):
        """Show individual file preview and approval"""
        try:
            files_to_process = []
            skipped_count = 0
            
            for file_info in files_to_rename:
                original_name = file_info['original_name']
                new_name = file_info['new_name']
                folder_path = file_info['folder_path']
                file_type = file_info['file_type']
                
                # Highlight problematic characters
                display_original = original_name
                problematic_chars = ['"', "'", '/', '\\', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '[', ']', '{', '}', ';', ':', '|', '<', '>', '?', ',', '.', '`', '~', ' ']
                problem_chars_found = []
                
                for char in problematic_chars:
                    if char in display_original:
                        if char == ' ':
                            problem_chars_found.append('SPACE')
                        else:
                            problem_chars_found.append(char)
                        display_original = display_original.replace(char, f'[{char}]')
                
                # Create preview message
                preview_msg = f'Type: {file_type}\\n'
                preview_msg += f'Location: {folder_path}\\n\\n'
                preview_msg += f'Current name: {display_original}\\n'
                preview_msg += f'New name: {new_name}\\n\\n'
                preview_msg += f'Problems found: {", ".join(problem_chars_found)}\\n\\n'
                preview_msg += f'Rename this file?\\n\\n'
                preview_msg += f'(File {len(files_to_process) + skipped_count + 1} of {len(files_to_rename)})'
                
                result = ui.messageBox(
                    preview_msg,
                    'Rename Cloud File?',
                    adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType
                )
                
                if result == adsk.core.DialogResults.DialogYes:
                    files_to_process.append(file_info)
                elif result == adsk.core.DialogResults.DialogNo:
                    skipped_count += 1
                else:  # Cancel
                    break
            
            # Confirm batch rename
            if files_to_process:
                summary_msg = f'Ready to rename {len(files_to_process)} cloud files'
                if skipped_count > 0:
                    summary_msg += f' (skipped {skipped_count})'
                summary_msg += '\\n\\nProceed with batch rename?'
                
                final_result = ui.messageBox(
                    summary_msg,
                    'Confirm Cloud File Rename',
                    adsk.core.MessageBoxButtonTypes.YesNoButtonType
                )
                
                if final_result == adsk.core.DialogResults.DialogYes:
                    self.perform_cloud_file_renames(ui, files_to_process)
                else:
                    ui.messageBox('Rename operation cancelled')
            else:
                ui.messageBox('No files selected for renaming')
                
        except:
            ui.messageBox('Preview failed:\n{}'.format(traceback.format_exc()))
    
    def perform_cloud_file_renames(self, ui, files_to_rename):
        """Perform the actual cloud file renames"""
        renamed_count = 0
        failed_files = []
        
        for file_info in files_to_rename:
            try:
                data_file = file_info['data_file']
                new_name = file_info['new_name']
                
                # Rename the cloud file
                data_file.name = new_name
                renamed_count += 1
                
            except Exception as e:
                failed_files.append(f"{file_info['original_name']}: {str(e)}")
        
        # Show results
        result_message = f'Successfully renamed {renamed_count} of {len(files_to_rename)} cloud files'
        
        if failed_files:
            result_message += f'\\n\\nFailed to rename {len(failed_files)} files:'
            for failure in failed_files[:5]:  # Show first 5 failures
                result_message += f'\\n- {failure}'
            if len(failed_files) > 5:
                result_message += f'\\n... and {len(failed_files) - 5} more'
        
        ui.messageBox(result_message)
    
    def clean_filename(self, filename, replace_spaces, replace_special, replace_unicode, to_lowercase, replacement_char):
        """Clean a filename by replacing special characters"""
        cleaned = filename
        
        # Convert to lowercase first if requested
        if to_lowercase:
            cleaned = cleaned.lower()
        
        # Replace spaces
        if replace_spaces:
            cleaned = cleaned.replace(' ', replacement_char)
        
        # Replace special characters (including quotes and slashes)
        if replace_special:
            special_chars = r'[!@#$%^&*()+=\[\]{};:"|<>?,./\\`~\'"]'
            cleaned = re.sub(special_chars, replacement_char, cleaned)
        
        # Replace unicode characters (keep only ASCII)
        if replace_unicode:
            cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
        
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