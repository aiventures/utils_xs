
@echo off
rem env_set.bat [var] [value] sets a value and stores it in path MY_P_MYENV/var 

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1
if %NUM_ARGS% NEQ 2 (
    
    goto end

)

:: Now run the command saved from python program

echo %C_O%
cat %MY_F_COLORS_PY%
goto end

:end



