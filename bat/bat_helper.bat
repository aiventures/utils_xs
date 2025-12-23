@echo off 
rem bat_helper.bat wrapper around bat_helper.py

rem activate variables and virtuakl environment 
call setenv.bat
call vas.bat

if not defined MY_P_MYENV (
    echo %C_E%Path MY_P_MYENV to store variables is not defined%C_0%
    goto end
)

if not defined MY_P_UTILS_SCRIPTS (
    echo %C_E%Path MY_P_UTILS_SCRIPTS containing scripts is not defined%C_0%
    goto end
)

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1

@REM if %NUM_ARGS% EQU 1 if not defined %1 (
@REM     echo %C_W%env_set.bat [var], %1 is not a valid environment name to get a value%C_0%
@REM     goto end    
@REM )

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

rem save the environment variable
set "py_prog=%MY_P_UTILS_SCRIPTS%\bat_helper.py"
python %py_prog% %*

:end
echo %C_0%


