@echo off
rem bat_list.bat [path_list|default MY_P_UTILS_BAT] show bat files for selection (bat_list.py) 
:: Count number of arguments
set pwd=%CD%
set num_args=0
for %%x in (%*) do set /A num_args+=1

:continue
call colors.bat %*
call myenv.bat %*
set "py_program=%MY_P_UTILS_SCRIPTS%\bat_list.py"
set "p_bat=%MY_P_UTILS_BAT%"

rem show info on run programs
echo %C_T%### RUN %C_PROG%%~f0%C_PY%
echo %C_T%Run Python Program %C_PY%%py_program% with params%C_H% [%*]%C_0%

rem handle up to 4 goal-based arguments
if not "%~4"=="" goto args1
if not "%~3"=="" goto args1
if not "%~2"=="" goto args1
if not "%~1"=="" goto args1

rem run without commands 
:run_without_args
echo no args
goto end

:args1
rem your code for arg1 here
echo args1
set "p_bat=%1"
goto end

:args2
rem your code for arg2 here
echo args2
goto end

:args3
rem your code for arg3 here
echo args3
goto end

:args4
rem your code for arg4 here
echo args4
goto end

:end
rem show the dialogue with the available paths
python "%py_program%" --paths "%p_bat%"
rem run the command if there is one 
set /p my_cmd=< %MY_F_MYENV_CMD%
echo %C_H%RUN COMMAND%C_PY% %my_cmd% %C_0%
%my_cmd%
set myenv_cmd=
set num_args=
set pwd=
set py_program=
set p_bat=
echo %C_0%
