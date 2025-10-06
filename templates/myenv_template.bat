@echo off
rem myenv.bat setting local env variables with MY_ prefix 
rem working venv with additional Libraries
rem place this file to /bat folder and adapt the variables 
rem use bat2py to create a file containing these variables as python constants

call colors.bat

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1
if %NUM_ARGS% gtr 0 echo %COL_GREY_DARK%### RUN %~f0%C_0%

rem Windows Desktop
set "MY_P_DESKTOP=C:\Users\<YOUR_USER>\Desktop"
rem working path set accordingly
set "MY_P_WORK=C:\<Path to a working directory>"
rem repo paths
set "MY_P_REPO=%MY_P_WORK%\WORK"
rem path to python installation
set "MY_P_PYTHON=C:\<Path To>\Python"
rem path to utils repo
set "MY_P_UTILS=%MY_P_WORK%\<path to>\utils_xs"
rem path to utils bat scripts 
set "MY_P_UTILS_BAT=%MY_P_UTILS%\bat"
rem path to utils python scripts 
set "MY_P_UTILS_SCRIPTS=%MY_P_UTILS%\src\scripts"
rem path to utils config folder
set "MY_P_UTILS_CONFIG=%MY_P_UTILS%\src\config"
rem path containing venvs
set "MY_P_VENV=%MY_P_WORK%\VENV"
rem path containing work venv 
set "MY_P_VENV_WORK=%MY_P_VENV%\utils_xs"
rem path to store locally buffered environment variables 
rem so as to store them from python to command line
set "MY_P_MYENV=%MY_P_WORK%\MYENV"
rem location of prompt file 
set "MY_F_MYENV_PROMPT=%MY_P_MYENV%\prompt.env"
rem file containing a bat command call cmd ... generated from python side
set "MY_F_MYENV_CMD=%MY_P_MYENV%\cmd_bat_list.env"
rem VSCODE Project Location
set "MY_P_VSCODE_PROJECTS=%MY_P_WORK%\vscode_workspaces"
rem My Default VSCOE Project 
set "MY_F_VSCODE_PROJECT=%MY_P_VSCODE_PROJECTS%\utils_xs.code-workspace"
rem BAT File containing MYENV Variables (this file)
set "MY_F_MYENV_BAT=%MY_P_UTILS_BAT%\myenv.bat"
rem PY File containing MYENV Variables (converted using convert_bat_env_to_python.py)
set "MY_F_MYENV_PY=%MY_P_UTILS_CONFIG%\myenv.py"
rem BAT File containing color codes 
set "MY_F_COLORS_BAT=%MY_P_UTILS_BAT%\colors.bat"
rem PY File containing Color Variables (converted using convert_bat_colors_to_python.py)
set "MY_F_COLORS_PY=%MY_P_UTILS_CONFIG%\colors.py"
rem Path to EXIFTOOL executable
set "MY_CMD_EXIFTOOL=C:\<path_to\ExifTool\exiftool.exe"
rem Path to Image Folder Dump 
set "MY_P_PHOTOS_TRANSIENT=C:\<path_to>\PhotosTransient"
rem Root Path to place Photo Folders 
set "MY_P_PHOTO_OUTPUT_ROOT=%MY_P_PHOTOS_TRANSIENT%\PHOTOS"
rem Path where to place Images from Camera 
set "MY_P_PHOTO_DUMP=%MY_P_PHOTO_OUTPUT_ROOT%\_DUMP"
