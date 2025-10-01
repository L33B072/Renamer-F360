import adsk.core
import adsk.fusion
import traceback
import re

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        ui.messageBox('Cloud File Renamer is starting...')
        
        # Get the data manager to access cloud files
        data_mgr = app.data
        
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
        
        # Scan the project for files that need renaming
        files_to_rename = scan_project_for_files(current_project)
        
        if not files_to_rename:
            ui.messageBox('No files with special characters found in this project.')
            return
        
        # Show results and process files
        message = f'Found {len(files_to_rename)} files with special characters:\\n\\n'
        for i, file_info in enumerate(files_to_rename[:5]):  # Show first 5
            message += f'{i+1}. {file_info["original_name"]} → {file_info["new_name"]}\\n'
        
        if len(files_to_rename) > 5:
            message += f'... and {len(files_to_rename) - 5} more files\\n'
        
        message += '\\n\\nRename all these files?'
        
        result = ui.messageBox(message, 'Rename Cloud Files', adsk.core.MessageBoxButtonTypes.YesNoButtonType)
        
        if result == adsk.core.DialogResults.DialogYes:
            # Perform the renames
            renamed_count = 0
            failed_count = 0
            
            for file_info in files_to_rename:
                try:
                    data_file = file_info['data_file']
                    data_file.name = file_info['new_name']
                    renamed_count += 1
                except:
                    failed_count += 1
            
            result_msg = f'Renamed {renamed_count} files successfully'
            if failed_count > 0:
                result_msg += f'\\n{failed_count} files could not be renamed'
            
            ui.messageBox(result_msg)
        
    except:
        if ui:
            ui.messageBox('Error in Cloud File Renamer:\\n{}'.format(traceback.format_exc()))

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
                files_to_rename.append({
                    'data_file': data_file,
                    'original_name': original_name,
                    'new_name': cleaned_name
                })
        
        # Scan subfolders
        sub_folders = folder.dataFolders
        for i in range(sub_folders.count):
            sub_folder = sub_folders.item(i)
            scan_folder_recursive(sub_folder, files_to_rename)
    except:
        pass

def clean_filename(filename):
    """Clean filename by replacing problematic characters"""
    cleaned = filename
    
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    
    # Replace special characters including quotes and slashes
    special_chars = r'[!@#$%^&*()+=\[\]{};:"|<>?,./\\`~\'"]'
    cleaned = re.sub(special_chars, '_', cleaned)
    
    # Replace unicode characters (keep only ASCII)
    cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
    
    # Clean up multiple consecutive underscores
    cleaned = re.sub('_+', '_', cleaned)
    
    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')
    
    # Ensure we don't have an empty filename
    if not cleaned:
        cleaned = 'unnamed_file'
    
    return cleaned