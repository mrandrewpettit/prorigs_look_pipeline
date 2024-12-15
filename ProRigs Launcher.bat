@echo off
cd /d "%~dp0"

REM Activate the virtual environment (assuming it's in the same folder as the batch file)
call .venv\Scripts\activate.bat

REM Set environment variables
set PRG_ROOT=%~dp0

set PRG_TOOLS=%PRG_ROOT%tools
set PRG_PYTHON_LIBS=%PRG_TOOLS%src
set PRG_MAYA=%PRG_TOOLS%software\maya
set PRG_MAYA_PROJECT=%PRG_MAYA%common\projects\ProRigs
set PRG_MAYA_SCENES=%PRG_MAYA_PROJECT%scenes
set PRG_MAYA_SOURCEIMAGES=%PRG_MAYA_PROJECT%sourceimages

REM User defined custom environment variables
set AUTODESK_ROOT=C:\Program Files\Autodesk
set SIDEFX_ROOT=C:\Program Files\Side Effects Software
set SUBSTANCE_PAINTER_ROOT=E:\SteamLibrary\steamapps\common
set PRG_ASSETS=%PRG_ROOT%assets

REM Navigate to the Python script's directory
cd /d "%PRG_TOOLS%\src\prorigs"

REM Run the Python script
python main.py
