# Running Back Fantasy Point Distribution

This project analyzes NFL running back performance data and creates a histogram as well as a box and whisker plot to visualize said data. It is built with Python and uses the uv package manager to manage the depndencies and virtual environments.

## Quick Start
If you just want to run the program without setting up a development environment, you can use the standalone executable. Simply download the executable from the releases page and run `RB_Stats.exe`.

*This version has all dependencies (pandas, nflreadpy, etc.) built-in and does not require Python to be installed on your system.*

---

## Development Setup

If you want to edit the code or run it from the source, follow these steps:

### 1. Install uv
This project relies on uv to manage dependencies. If you don't have it installed, run the following command in PowerShell:
```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```
### 2. Run the Program
You do not need to manually create a virtual environment or install libraries via pip. Simply run:
```powershell
uv run main.py
```
uv will automatically read the uv.lock file, download the required Python version, create a virtual environment, and install all dependencies in the background.

---

## Building the Executable (.exe)

If you wish to re-build the executable using PyInstaller, uv handles the environment for you. You have two options for how you would like to build the executable.

Option 1: Standalone File (Slower but useful for demonstration purposes or sharing) Bundles all of the dependencies into the executable. Note that it may take a few seconds to start as it unpacks dependencies (which must happen each and every time the program is run).
```powershell
uv run pyinstaller --onefile --clean main.py
```

Option 2: Directory Bundle (Faster startup) Creates a folder with the .exe and dependencies separated. This runs faster but the .exe cannot be moved out of its folder.
```powershell
uv run pyinstaller --onedir --clean main.py
```

---

## Troubleshooting

Execution Policy Error

If you see an error stating that "running scripts is disabled on this system" when trying to install uv or run scripts, you can bypass this:

Temporarily (Current window only):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Permanently (Your user account):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---


## Dependencies

* nflreadpy
* pyarrow
* pandas
* numpy
* matplotlib
* seaborn
* scipy

---

## Author
**Dominic Murray**
