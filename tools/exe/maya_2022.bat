@echo off

if "%1" == "BATCH" (
	set MAYA_BATCH=TRUE
	shift /1
)

set MAYA_VER=2022

call %~dp0\..\software\maya\LaunchMaya.bat %1 %2 %3 %4

endlocal