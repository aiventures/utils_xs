@echo off
rem myenv.bat setting local env variables with MY_ prefix 
rem working venv with additional Libraries
rem place this file to /bat folder and adapt the variables 
rem use bat2py to create a file containing these variables as python constants

rem set unicode code page to display special characters
chcp 65001 >NUL

rem will only be called once 
call colors.bat

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1

rem if already initialized and no params are supplied skip execution
if defined MY_SETENV_CALLED if %NUM_ARGS% EQU 0 ( goto end )

echo %COL_GREY_DARK%### RUN %~f0%C_0%

rem flag that setenv was called
set MY_SETENV_CALLED=1
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
set "MY_F_MYENV_BAT=%MY_P_UTILS_BAT%\setenv.bat"
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
rem Path containing templates
set "MY_P_UTILS_TEMPLATES=%MY_P_UTILS%\templates"
rem Path to Python SCRIPT for video series rename 
set "MY_PY_VIDEO_RENAME=%MY_P_UTILS_SCRIPTS%\video_rename.py"
rem Path containing Waypoint Template, see https://exiftool.org/geotag.html
rem command exiftool exiftool -p %MY_F_EXIFTOOL_WPT% *.jpg
set "MY_F_EXIFTOOL_WPT=%MY_P_UTILS_TEMPLATES%\exiftool_wpt.fmt"
rem Here's the Defintions for EXIFTOOL Utility which are picked up from the exiftool utility
rem this is your name and title / used in /src/scripts/image_organizer.py
set "MY_EXIFTOOL_AUTHOR=HUGOAUTHOR" 
set "MY_EXIFTOOL_AUTHORTITLE=The Honoroable" 
rem FIXED LOCATION FOR IMAGES DUNP
set "MY_P_EXIFTOOL_DUMP=C:\<path_to_folder_containing_dump_of_raw_image_files>" 
rem FIXED LOCATION TO COPY IMAGES BY DATEs
set "MY_P_EXIFTOOL_TARGET=C:\<path_to_temp_folder_containing_files_by_date>"
rem LOGLEVEL FOR PRINTING /libs/custom_print.py (USED IN EXIFTOOL UTILITY, VALUES OF DEBUG INFO WARNING ERROR )
set "MY_PRINT_LEVEL=DEBUG" 

rem call the default environment directly
call "%MY_P_VENV_WORK%\Scripts\activate.bat"
call p.bat

:end