@echo off 
rem env_save.bat [name] [value or existing environment var] saves an environment value into folder MY_P_MYENV (env_helper.py)
rem equ	gleich
rem neq	ungleich
rem lss	kleiner als
rem leq	kleiner/gleich
rem gtr	größer als
rem geq	größer gleich

rem activate variables and virtual environment 
call setenv.bat


:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1

if %NUM_ARGS% EQU 1 if not defined %1 (
    echo %C_W%env_set.bat [var], %1 is not a valid environment name to get a value%C_0%
    goto end    
)

if %NUM_ARGS% EQU 0 (
    echo %C_W%env_set.bat [var] [value], at least one param required%C_0%
    goto end
)

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

if not defined MY_P_MYENV (
    echo %C_E%Path MY_P_MYENV to store variables is not defined%C_0%
    goto end
)

if not defined MY_P_UTILS_SCRIPTS (
    echo %C_E%Path MY_P_UTILS_SCRIPTS containing scripts is not defined%C_0%
    goto end
)

rem save the environment variable
set "py_prog=%MY_P_UTILS_SCRIPTS%\env_helper.py"
python %py_prog% --action-save-env --p-output %MY_P_MYENV% --params "%*"

:end
set params=
set value=
set py_prog=
echo %C_0%


