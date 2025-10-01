# Fusion 360 File Renamer Add-in

A Fusion 360 add-in that scans through all file names in a Fusion 360 project and renames files containing special characters with clean, standard characters.

## Features

- **Automatic Scanning**: Scans all components and files in the active Fusion 360 project
- **Special Character Detection**: Identifies files with spaces, special characters (!@#$%^&*), and unicode characters
- **Batch Renaming**: Rename multiple files at once with a single operation
- **Preview Changes**: See exactly what changes will be made before applying them
- **Customizable Replacement**: Choose your preferred replacement character (default: underscore)
- **Safe Operation**: Preserves file relationships and references within Fusion 360

## Installation

1. Download the add-in files
2. Copy the entire `FileRenamer` folder to your Fusion 360 add-ins directory:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
3. Copy the `manifest` file to the same add-ins directory
4. Restart Fusion 360
5. Enable the add-in from the Scripts and Add-Ins dialog

## Usage

1. Open a Fusion 360 project with files that need renaming
2. Navigate to the **Modify** panel in the toolbar
3. Click the **Rename Files** button
4. Configure your renaming options:
   - Replace spaces with underscores
   - Replace special characters
   - Replace unicode characters
   - Convert to lowercase
   - Custom replacement character
5. Review the preview of changes
6. Click **Execute** to apply the changes

## Character Replacement Rules

### Default Behavior
- **Spaces** → Underscores (`_`)
- **Special Characters** (`!@#$%^&*()+=[]{};"'|<>?,.\/\`~`) → Underscores (`_`)
- **Unicode Characters** → Removed or replaced with underscores
- **Multiple consecutive replacements** → Single replacement character
- **Leading/trailing replacements** → Removed

### Examples
- `My Project File.f3d` → `My_Project_File.f3d`
- `Component (v2).ipt` → `Component_v2_.ipt`
- `测试文件.step` → `_.step` (unicode removed)
- `File!!!Name` → `File_Name`

## File Types Supported

The add-in works with:
- Fusion 360 components and assemblies
- Referenced files and documents
- Imported geometry and sketches
- Any named elements within the project

## Safety Features

- **Preview Mode**: Always shows changes before applying them
- **Validation**: Checks for valid filenames and system restrictions
- **Error Handling**: Graceful handling of rename failures
- **Preservation**: Maintains file relationships and references

## Troubleshooting

### Common Issues

**Add-in doesn't appear in toolbar**
- Verify files are in correct add-ins directory
- Check that manifest file is present
- Restart Fusion 360 completely
- Enable add-in in Scripts and Add-Ins dialog

**Rename operation fails**
- Some files may be read-only or locked
- Check file permissions
- Ensure project is not shared/locked by another user

**Preview shows no files**
- Project may already have clean filenames
- Check if special character detection options are enabled

### Error Messages

If you encounter errors, the add-in will display descriptive messages. Common solutions:
- Save your project before running the add-in
- Ensure you have write permissions to the project
- Close any external references to the files being renamed

## Development

### Project Structure
```
FileRenamer/
├── FileRenamer.py          # Main add-in entry point
├── commands/
│   ├── __init__.py
│   └── RenameFilesCommand.py   # Main command implementation
├── lib/
│   ├── __init__.py
│   └── file_utils.py       # Utility functions for file operations
└── resources/              # UI resources and icons
```

### API References
- [Fusion 360 API Documentation](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [Python API Reference](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-7B5A90C8-E94C-48DA-B16B-430729B734DC)

## License

This add-in is provided as-is for educational and development purposes. Please test thoroughly before using in production environments.

## Version History

- **v1.0.0**: Initial release with basic file renaming functionality