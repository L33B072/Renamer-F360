# Fusion 360 Cloud File Renamer - Installation Guide

## Quick Start

Follow these steps to install and use the Fusion 360 Cloud File Renamer scripts:

### Option 1: Run Scripts Directly (Recommended)

**No installation required!** Simply download and run:

1. **Download the script files:**
   - `SimpleCloudRenamer.py` (for basic use)
   - `CloudFileRenamer.py` (for advanced features)

2. **Open Fusion 360** and load a project with files to rename

3. **Run the script:**
   - Press **Shift+S** or go to **Tools > Scripts and Add-Ins**
   - Click the **Scripts** tab
   - Click the **green "+" button**
   - Browse and select your downloaded script file
   - Click **Run**

### Option 2: Install to Scripts Folder

For permanent access without browsing each time:

1. **Locate your Fusion 360 Scripts directory:**
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`

2. **Copy the script files:**
   - Copy `SimpleCloudRenamer.py` and/or `CloudFileRenamer.py` to the Scripts directory

3. **Access from Scripts menu:**
   - Scripts will appear in the Scripts and Add-Ins dialog for easy access

## Usage

### SimpleCloudRenamer.py
**Best for beginners:**
1. Open a Fusion 360 project with files that need renaming
2. Run the script (using either method above)
3. Review the list of files to be renamed
4. Click "Yes" to proceed with bulk rename

### CloudFileRenamer.py
**Advanced features:**
1. Open a Fusion 360 project with files that need renaming
2. Run the script (using either method above)
3. Review each file individually:
   - See problematic characters highlighted
   - Choose Yes/No/Cancel for each file
   - View folder path for each file
4. Confirm final batch operation
5. Review detailed results

## Troubleshooting

### "Please open a document first" error
- Make sure you have a Fusion 360 project/document open before running the script
- The script needs access to a project to scan cloud files

### Script doesn't find any files
- Your project may already have clean filenames
- Check that files actually contain spaces or special characters
- Try with a project that has files like "My File (v2).f3d"

### Some files fail to rename
- Files may be in use by other users in shared projects
- Some files might be read-only or locked
- Check the detailed error messages provided by the script

### Script takes a long time
- Large projects with many nested folders take time to scan
- Wait for the script to complete its recursive scanning
- The script will show progress messages

## Testing

Run the included test script to verify the filename cleaning logic:
```bash
python test_utilities.py
```

This tests the core filename cleaning functions without requiring Fusion 360.

## Which Script Should I Use?

- **New users**: Start with `SimpleCloudRenamer.py` - it's straightforward and handles most use cases
- **Advanced users**: Use `CloudFileRenamer.py` for detailed control and preview of each file
- **Large projects**: `SimpleCloudRenamer.py` is faster for bulk operations
- **Selective renaming**: `CloudFileRenamer.py` lets you approve each file individually

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Fusion 360 version is supported
3. Test with the included test script first
4. Check the Fusion 360 console for error messages