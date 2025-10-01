# Fusion 360 Cloud File Renamer Scripts

Fusion 360 Python scripts that scan through all file names in your cloud projects and rename files containing special characters with clean, standard characters.

## Features

- **Cloud File Support**: Works directly with Fusion 360's cloud-based file system
- **Automatic Scanning**: Recursively scans all folders and files in the active project
- **Special Character Detection**: Identifies files with spaces, special characters (!@#$%^&*), and unicode characters
- **Individual File Preview**: Review each file individually before renaming
- **Batch Operations**: Apply changes to multiple approved files at once
- **Safe Operation**: Shows exactly what changes will be made with problematic characters highlighted
- **Error Handling**: Graceful handling of rename failures with detailed feedback

## Available Scripts

### 1. SimpleCloudRenamer.py
**Best for beginners** - A streamlined script that:
- Uses default settings (replaces spaces and special chars with underscores)
- Shows a simple list of all files to be renamed
- Performs bulk rename with one confirmation dialog

### 2. CloudFileRenamer.py  
**Advanced version** - Full-featured script that:
- Shows individual file previews with problematic characters highlighted
- Allows per-file approval (Yes/No/Cancel for each file)
- Displays folder paths for each file
- Provides detailed rename results and error reporting

## Installation & Usage

### Method 1: Run as Scripts (Recommended)
1. **Download** the script folders (`SimpleCloudRenamer/` and/or `CloudFileRenamer/`)
   - Each folder contains both the `.py` script file and `.manifest` file
2. **Open Fusion 360** and click into a project with files that need renaming
3. **Open one file** from the project that contains data
4. **Open Scripts and Add-Ins** (Shift+S or Tools menu)
5. **Go to Scripts tab**
6. **Click the green "+" button** and browse to select the script folder
7. **Click "Run"** to execute the script

### Method 2: Add to Scripts Folder
1. Copy the script folders to your Fusion 360 Scripts directory:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
   - Copy entire folders: `SimpleCloudRenamer/` and/or `CloudFileRenamer/`
2. Scripts will appear in the Scripts and Add-Ins dialog for easy access

## How It Works

1. **Open a project** in Fusion 360 that contains files with special characters
2. **Run the script** through Scripts and Add-Ins
3. **Script scans** your entire project recursively through all folders
4. **Review files** - script shows you each problematic file with issues highlighted
5. **Approve changes** - choose which files to rename
6. **Batch rename** - all approved files are renamed in Fusion 360's cloud storage

## Character Replacement Rules

### Default Behavior
- **Spaces** → Underscores (`_`)
- **Special Characters** (`!@#$%^&*()+=[]{};"'|<>?,.\/\`~`) → Underscores (`_`)
- **Unicode Characters** → Removed (keeps only ASCII characters)
- **Multiple consecutive replacements** → Single replacement character
- **Leading/trailing replacements** → Removed

### Examples
- `My Project File.f3d` → `My_Project_File.f3d`
- `Component (v2).ipt` → `Component_v2_.ipt`
- `测试文件.step` → `unnamed_file.step` (unicode removed)
- `File!!!Name` → `File_Name`
- `"Bad/File\Name"` → `Bad_File_Name`

## Supported File Types

The scripts work with all file types in Fusion 360's cloud storage:
- Fusion 360 design files (.f3d)
- CAD files (.step, .iges, .sat, etc.)
- Drawing files (.dwg, .dxf)
- Image and document files
- Any files stored in your Fusion 360 project folders

## Safety Features

- **Individual Preview**: See exactly what each file will be renamed to
- **Approval Required**: Scripts never rename files without your explicit approval
- **Error Handling**: Graceful handling of files that can't be renamed
- **Detailed Results**: Shows success/failure status for each operation
- **Non-destructive**: Only changes file names, never file content

## Troubleshooting

### Common Issues

**"Please open a document first" error**
- Make sure you have a Fusion 360 project/document open before running the script
- The script needs access to the current project to scan files

**Script doesn't find any files**
- Your project may already have clean filenames
- Check that files actually contain spaces or special characters

**Some files fail to rename**
- Files may be in use by other users in shared projects
- Some files might be read-only or locked
- Check the detailed error messages provided by the script

**Script appears to hang**
- Large projects with many files may take time to scan
- Wait for the script to complete its recursive folder scanning

### Error Messages

The scripts provide detailed error messages. Common solutions:
- Ensure you have edit permissions for the project
- Make sure files aren't currently open in other applications
- Try running the script again if network issues caused failures

## Development

### Repository Structure
```
Renamer-F360/
├── SimpleCloudRenamer/          # Simple script folder
│   ├── SimpleCloudRenamer.py    # Simple version for basic use
│   └── SimpleCloudRenamer.manifest # Script manifest file
├── CloudFileRenamer/            # Advanced script folder  
│   ├── CloudFileRenamer.py      # Advanced version with full preview
│   └── CloudFileRenamer.manifest   # Script manifest file
├── test_utilities.py            # Test file for validation
├── manifest                     # Legacy add-in manifest file
├── INSTALL.md                  # Installation instructions
└── README.md                   # This file
```

### Testing
Run `test_utilities.py` to validate the filename cleaning functions:
```python
python test_utilities.py
```

### API References
- [Fusion 360 API Documentation](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [Fusion 360 Data Management API](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-BD6B2B0C-F982-41C8-94DC-F15C8B9A75C8)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve these scripts.

## License

This project is provided as-is for educational and development purposes. Please test thoroughly before using in production environments.

## Version History

- **v2.0.0**: Simplified to script-based approach, added cloud file support
- **v1.5.0**: Added individual file preview and approval
- **v1.0.0**: Initial add-in release
