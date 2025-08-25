# Packaging CSV Populator as Standalone Windows Executable

This guide will help you package your CSV Populator Python application into a standalone Windows executable that users can run without installing Python.

## Quick Start

### Option 1: Use the Build Script (Easiest)

1. **Double-click `build.bat`** - This will automatically:
   - Check if Python is installed
   - Install PyInstaller if needed
   - Build your executable
   - Show you where the file is created

### Option 2: Manual Build

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Run the build script:**

   ```bash
   python build_exe.py
   ```

3. **Or use PyInstaller directly:**
   ```bash
   pyinstaller --onefile --windowed --name=CSV_Populator csv_populator.py
   ```

## What Gets Created

After building, you'll find:

- `dist/CSV_Populator.exe` - Your standalone executable
- `build/` - Temporary build files (can be deleted)
- `CSV_Populator.spec` - Build configuration file

## File Size

The resulting executable will be approximately:

- **Basic build**: 15-25 MB
- **Optimized build**: 10-20 MB (using the .spec file)

## Distribution

Your users will be able to:

1. Download the `CSV_Populator.exe` file
2. Double-click to run immediately
3. Use all features (CSV generation, templates, etc.)
4. No Python knowledge required!

## Troubleshooting

### Common Issues

1. **"PyInstaller not found"**

   - Run: `pip install pyinstaller`

2. **Build fails with import errors**

   - The build script handles most common cases
   - Check that all imports in your code are standard library

3. **Executable is very large**
   - Use the .spec file for better optimization
   - The excludes list removes unnecessary libraries

## Testing Your Executable

1. **Test on your machine first**
2. **Test on a clean Windows machine** (no Python)
3. **Test all features** - CSV generation, templates, etc.

## Support

The build script includes error handling and will guide you through most issues. The resulting executable should work on:

- Windows 10/11 (64-bit)
- Windows 8.1 (64-bit)
- Windows 7 (64-bit) - may require additional dependencies

Your users will have a professional, standalone application that works just like any other Windows program!
