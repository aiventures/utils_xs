@echo off 
rem env_get.bat [name] reads content of a file named [name] in environment folder MY_P_MYENV
rem equ	gleich
rem neq	ungleich
rem lss	kleiner als
rem leq	kleiner/gleich
rem gtr	größer als
rem geq	größer gleich

rem activate variables and virtuakl environment 
rem activate variables and virtual environment 
call setenv.bat


:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1
if %NUM_ARGS% LEQ 0 (
    echo %C_W%env_get.bat [envname], at least one params required%C_0%
    goto end
)

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

if not defined MY_P_MYENV (
    echo %C_E%Path MY_P_MYENV to store variables is not defined%C_0%
    goto end
)

set env_name=%1
set env_path=%MY_P_MYENV%\%env_name%

if not exist %env_path% (    
    echo %C_E%No Env Variable named [%env_path%], skip reading, variables%C_0%
    ls %MY_P_MYENV%
    goto end
)

set /p %env_name%=<"%env_path%"
set /p value=<"%env_path%"
echo %C_I%SET %C_F%[%env_name%]%C_PY%: (%value%)%C_0%

:end
set value=


