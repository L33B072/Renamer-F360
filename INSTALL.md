# Fusion 360 File Renamer - Installation Guide

## Quick Start

Follow these steps to install and use the Fusion 360 File Renamer add-in:

### 1. Installation

1. **Locate your Fusion 360 Add-ins directory:**
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

2. **Copy the files:**
   - Copy the entire `FileRenamer` folder to the add-ins directory
   - Copy the `manifest` file to the same add-ins directory

3. **Directory structure should look like:**
   ```
   AddIns/
   ├── manifest
   └── FileRenamer/
       ├── FileRenamer.py
       ├── commands/
       ├── lib/
       └── resources/
   ```

   **Note**: If you cloned this repository, the files are in the `Renamer-F360` folder.

### 2. Enable the Add-in

1. Open Fusion 360
2. Go to **Utilities** → **Scripts and Add-Ins** (or press Shift+S)
3. Click the **Add-Ins** tab
4. Find "File Renamer" in the list
5. Click **Run** to enable it temporarily, or **Run on Startup** for permanent installation

### 3. Using the Add-in

1. Open a Fusion 360 project with files that need renaming
2. Go to the **Modify** panel in the Design workspace
3. Look for the **Rename Files** button
4. Click it to open the renaming dialog
5. Configure your options and click **Execute**

## Troubleshooting

### Add-in doesn't appear
- Verify file locations are correct
- Restart Fusion 360 completely
- Check that the `manifest` file is in the root add-ins directory
- Enable the add-in from Scripts and Add-Ins dialog

### Python errors
- The add-in requires Python 3.7+ (included with Fusion 360)
- Check that all files were copied correctly
- Look at the Fusion 360 console for detailed error messages

### No files found to rename
- Make sure your project has components with special characters
- Check that the detection options are enabled
- Try with a project that has files with spaces or special characters

## Testing

Run the included test script to verify functionality:
```bash
python test_utilities.py
```

This will test the core file renaming logic without requiring Fusion 360.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Fusion 360 version is supported
3. Test with the included test script first
4. Check the Fusion 360 console for error messages