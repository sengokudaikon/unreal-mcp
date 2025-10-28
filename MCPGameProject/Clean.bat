@echo off
REM Clean build artifacts for MCPGameProject

setlocal

set PROJECT_ROOT=%~dp0

echo Cleaning MCPGameProject build artifacts...
echo.

REM Remove build folders
if exist "%PROJECT_ROOT%Binaries" (
    echo Removing Binaries...
    rmdir /s /q "%PROJECT_ROOT%Binaries"
)

if exist "%PROJECT_ROOT%Intermediate" (
    echo Removing Intermediate...
    rmdir /s /q "%PROJECT_ROOT%Intermediate"
)

if exist "%PROJECT_ROOT%Saved\Logs" (
    echo Cleaning logs...
    del /q "%PROJECT_ROOT%Saved\Logs\*.*"
)

REM Clean plugin build artifacts
if exist "%PROJECT_ROOT%Plugins\UnrealMCPPlugin\Binaries" (
    echo Removing Plugin Binaries...
    rmdir /s /q "%PROJECT_ROOT%Plugins\UnrealMCPPlugin\Binaries"
)

if exist "%PROJECT_ROOT%Plugins\UnrealMCPPlugin\Intermediate" (
    echo Removing Plugin Intermediate...
    rmdir /s /q "%PROJECT_ROOT%Plugins\UnrealMCPPlugin\Intermediate"
)

echo.
echo CLEAN COMPLETE
exit /b 0
