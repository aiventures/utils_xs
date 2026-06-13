@echo off
rem py_img_organizer.bat [output_path|optional] Calls Up Image organizer without options use -h or --help to show options (using setenv.bat MY_P_PHOTO_OUTPUT_ROOT  and MY_P_UTILS_SCRIPTS\image_organizer.py)

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

set pwd=%CD%
set "py_program="%MY_P_UTILS_SCRIPTS%\image_organizer.py""
rem set default path to current path 
set "path_input="%pwd%""
set "path_output="%MY_P_PHOTO_OUTPUT_ROOT%""
rem set a command string usually argparse arguments
set "cmd_params=%*"
set num_args=0
for %%x in (%*) do set /A num_args+=1

rem show info on run programs
:show_info
echo %C_T%### RUN %C_PROG%%~f0%C_0%
echo %C_T%Run Python Program %C_PY%%py_program% with params%C_H%%cmd_params%%C_0%
rem here's the command to run without params
goto end

:end

rem params in build_arg_parser ImageOrganizer build_arg_parser

rem also set print level here DEBUG,INFO,WARNING,LEVEL
rem set "MY_ENV_PRINT_LEVEL=DEBUG"
rem set "MY_ENV_PRINT_SHOW_EMOJI=true"

rem MY_PRINT_LEVEL DEBUG INFO WARNING ERROR is usuaklly set by setenv.bat but can be overrideden here
rem set MY_PRINT_LEVEL=DEBUG
rem in case no p_source is given then the current path is used
rem "cmd_params=--action_show_args -prepare -transform -change"
rem set "cmd_params=-prepare -transform -change"
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
