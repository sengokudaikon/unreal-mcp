@echo off
REM Build script for MCPGameProject
REM Automatically finds Unreal Engine installation and builds the project

setlocal

REM Set project paths
set PROJECT_ROOT=%~dp0
set PROJECT_FILE=%PROJECT_ROOT%MCPGameProject.uproject

REM Try to find Unreal Engine installation
set UE_ROOT=
if exist "C:\Program Files\Epic Games\UE_5.6" (
    set UE_ROOT=C:\Program Files\Epic Games\UE_5.6
) else if exist "C:\Program Files\Epic Games\UE_5.5" (
    set UE_ROOT=C:\Program Files\Epic Games\UE_5.5
) else if exist "C:\Program Files\Epic Games\UE_5.4" (
    set UE_ROOT=C:\Program Files\Epic Games\UE_5.4
) else (
    echo ERROR: Could not find Unreal Engine installation
    echo Please install UE 5.4, 5.5, or 5.6 to C:\Program Files\Epic Games\
    exit /b 1
)

echo Found Unreal Engine at: %UE_ROOT%
echo Building MCPGameProject...
echo.

REM Build the project
"%UE_ROOT%\Engine\Build\BatchFiles\Build.bat" MCPGameProjectEditor Win64 Development -Project="%PROJECT_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo BUILD FAILED with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
echo BUILD SUCCESSFUL
exit /b 0
