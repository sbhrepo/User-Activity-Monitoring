# Building an Executable

## Option 1: Using PyInstaller (Recommended for Distribution)

### Prerequisites
```
pip install pyinstaller
```

### Build
```
build.bat
```

This creates a standalone `.exe` file in the `dist` folder that doesn't require Python to be installed.

### The Executable
- **Location**: `dist\ServerActivityMonitor.exe`
- **Size**: ~150-200 MB (includes Python runtime)
- **Distribution**: Can be distributed to machines without Python installed

### Create Installer (Advanced)
To create a professional installer, use Inno Setup:
1. Download Inno Setup from http://www.jrsoftware.org/isdl.php
2. Create a .iss script that references `dist\ServerActivityMonitor.exe`
3. Compile with Inno Setup to create an MSI installer

## Option 2: Direct Python Execution (Development)

### Quick Start
```
setup.bat
run.bat
```

### Requirements
- Python 3.8+ must be installed
- Users run `python run.py` or `run.bat`

## Deployment Strategies

### For Tech-Savvy Users
- Distribute source code
- Users run setup.bat and run.bat

### For General Users
- Build .exe with PyInstaller
- Create installer with Inno Setup
- Users run the installer and launch from Start Menu

### For Network Deployment
- Package the dist folder with a simple installer
- Or use Group Policy to deploy on corporate networks

## File Size Comparison

| Method | Size | Setup Time | Python Required |
|--------|------|-----------|-----------------|
| Source + Python | ~500 MB | 5 min | Yes |
| PyInstaller .exe | ~200 MB | 1 min | No |
| Inno Setup Installer | ~100 MB | 1 min | No |

## Testing the Build

After building with `build.bat`:
```
dist\ServerActivityMonitor.exe
```

The executable will run the same application without needing Python installed.

## Cross-Compilation Note

These builds are for Windows 11. To build for other platforms:
- **macOS**: Use PyInstaller on a Mac with `pyinstaller --onefile src/main.py`
- **Linux**: Use PyInstaller on Linux - GUI will work with Qt libraries
