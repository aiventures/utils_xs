@echo off
rem py_img_cleanup_images_undo.bat Moves back files from subfolders in MY_P_EXIFTOOL_TARGET

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

set pwd=%CD%
set "py_program="%MY_P_UTILS_SCRIPTS%\image_organizer.py""
rem set default path to current path 
set "path_input="%pwd%""
set "path_output="%MY_P_PHOTO_OUTPUT_ROOT%""
rem set a command string usually argparse arguments
set "cmd_params= "
set num_args=0
for %%x in (%*) do set /A num_args+=1

rem show info on run programs
:show_info
echo %C_T%### RUN %C_PROG%%~f0%C_0%
echo %C_T%Run Python Program %C_PY%%py_program% with params%C_H% [%*]%C_0%

if %num_args% GTR 0 goto run_with_params
rem here's the command to run without params
goto end

:run_with_params
rem handle up to 4 goal-based arguments
if not "%~4"=="" goto args4
if not "%~3"=="" goto args3
if not "%~2"=="" goto args2
if not "%~1"=="" goto args1

:args4
rem your code for arg4 here
set "p4=%4"
set "cmd_params=%cmd_params% -p4 %4"
echo args4
rem as there are 4 args process param 3
goto args3

:args3
rem your code for arg3 here
echo args3
set "p3=%3"
set "cmd_params=%cmd_params% -p3 %3"
rem as there are 4 args process param 2
goto args2

:args2
rem your code for arg2 here
set "path_output=%2"
rem echo args2
set "cmd_params=%cmd_params% --output %path_output%"
rem as there are 2 args process param 1
goto args1

:args1
rem your code for arg1 here, usually 1st param should be path_input adjust otherwise
echo args1
set "path_input=%1"
set "cmd_params=%cmd_params% --input %path_input%"
rem python "%py_program%" --p1 "%MY_F_MYENV_BAT%" --output "%MY_F_MYENV_PY%"
goto end

:end

rem MY_PRINT_LEVEL DEBUG INFO WARNING ERROR is usuaklly set by setenv.bat but can be overrideden here
rem set MY_PRINT_LEVEL=DEBUG
rem MY_P_EXIFTOOL_TARGET (folder containing all images) is defined in setenv.bat
rem set "cmd_params=--action-cleanup-images --action-cleanup-images-undo --action-show-args --recursive -src %MY_P_EXIFTOOL_TARGET%"
set "cmd_params=--action-cleanup-images-undo --recursive -src %MY_P_EXIFTOOL_TARGET%"
echo %C_H%RUN %C_PY%%py_program% %cmd_params%%C_0%
python %py_program% %cmd_params%
set p1=
set p2=
set p3=
set p4=
set cmd_params=
set path_input=
set num_args=
set pwd=
set py_program=
echo %C_0%
