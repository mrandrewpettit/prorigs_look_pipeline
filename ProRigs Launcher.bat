@echo off
cd /d "%~dp0"

REM Activate the virtual environment (assuming it's in the same folder as the batch file)
call .venv\Scripts\activate.bat

REM Set environment variables
set PRG_ROOT=%~dp0
set PRG_TOOLS=%PRG_ROOT%\tools
set PRG_PYTHON_LIBS=%PRG_TOOLS%\src
set PRG_MAYA=%PRG_TOOLS%\software\maya

REM User defined custom environment variables
set AUTODESK_ROOT=C:\Program Files\Autodesk
set SIDEFX_ROOT=C:\Program Files\Side Effects Software
set SUBSTANCE_PAINTER_ROOT=E:\SteamLibrary\steamapps\common
set PRG_ASSETS=W:\prorigs\assets

REM Navigate to the Python script's directory
cd /d "%PRG_TOOLS%\src\prorigs"

REM Run the Python script
python main.py