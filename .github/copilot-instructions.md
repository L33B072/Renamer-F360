# Fusion 360 File Renamer Add-in

This workspace contains a Fusion 360 add-in that scans through all file names in a Fusion 360 project and renames files containing special characters with clean, standard characters.

## Project Structure
- `FileRenamer/` - Main add-in directory
- `manifest` - Add-in manifest file
- `FileRenamer.py` - Main add-in entry point
- `commands/` - Command implementations
- `lib/` - Helper libraries and utilities
- `resources/` - UI resources and icons

## Development Guidelines
- Follow Fusion 360 API best practices
- Use Python for add-in development
- Implement proper error handling for file operations
- Test with various special character scenarios
- Ensure backward compatibility with existing projects

## Key Features
- Scan all files in active Fusion 360 project
- Identify files with special characters
- Provide preview of proposed name changes
- Batch rename functionality
- Undo/rollback capability
- Character replacement mapping customization