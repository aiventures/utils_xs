@echo off
rem _template_py_args_path.bat use for copy & paste to call python scripts with multiple args. first arg is a path variable
:: Count number of arguments

@REM EQU: Equal to
@REM NEQ: Not equal to
@REM LSS: Less than
@REM LEQ: Less than or equal to
@REM GTR: Greater than

call colors.bat %*
call myenv.bat %*

set pwd=%CD%
set "py_program=%MY_P_UTILS_SCRIPTS%\xyz.py"
rem set default path to current path 
set "path=%pwd%"
rem set a command string usually argparse arguments
set "cmd_params= "
set num_args=0
for %%x in (%*) do set /A num_args+=1
if num_args GTR 0 goto run_with_params
rem heres the command to run without params
goto end

:run_with_params
rem show info on run programs
:show_info
echo %C_T%### RUN %C_PROG%%~f0%C_0%
echo %C_T%Run Python Program %C_PY%%py_program%with params%C_H% [%*]%C_0%

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
set "p2=%2"
echo args2
set "cmd_params=%cmd_params% -p2 %2"
rem as there are 2 args process param 1
goto args1

:args1
rem your code for arg1 here, usually 1st param should be path adjust otherwise
echo args1
set "p1=%1"
set "cmd_params=%cmd_params% -p1 %1"
set "path=%1"
rem python "%py_program%" --p1 "%MY_F_MYENV_BAT%" --output "%MY_F_MYENV_PY%"
goto end

:end
echo %C_H%RUN %C_PY%%py_program%%cmd_params%%C_0%
python %py_program%%cmd_params%
set cmd_params=
set p1=
set p2=
set p3=
set p4=
set path=
set num_args=
set pwd=
set py_program=
echo %C_0%
