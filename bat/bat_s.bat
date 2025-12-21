@echo off
rem bat_s.bat [search use ;: for and/or and eventually use quotations|optional] [path_list|default MY_P_UTILS_BAT] search bat files for selection (bat_list.py) 
:: Count number of arguments
set pwd=%CD%
set num_args=0
for %%x in (%*) do set /A num_args+=1

:continue
call colors.bat %*
rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat
set "py_program=%MY_P_UTILS_SCRIPTS%\bat_list.py"
rem set a default path
set "py_args=--paths "%MY_P_UTILS_BAT%""

rem show info on run programs
echo %C_T%### RUN %C_PROG%%~f0%C_PY%

rem no more params go to end
if %num_args% EQU 0 goto end
rem at least one param is given 
set "py_args=%py_args% --query %1"
if %num_args% EQU 1 goto end
rem at least two params are given 
set "py_args=--query %1 --paths %2"
goto end

:end
echo %C_H%RUN %C_PY%^[python "%py_program%" %py_args%]%C_0%
python "%py_program%" %py_args%
rem run the command stored in the variable 
set /p my_cmd=< %MY_F_MYENV_CMD%
call %my_cmd%
set num_args=
set pwd=
set py_program=
set p_bat=
set my_cmd=
echo %C_0%
