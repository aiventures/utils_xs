@echo off
rem vd.bat  - deactivate VENV if activated and trigger update of prompt 

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

if not defined VIRTUAL_ENV (
    echo %C_W%No VENV environment is activated%C_0%
    goto end
)

rem deactivate environment
echo %C_I%Deactivating VENV [%VIRTUAL_ENV%]%C_0%
deactivate

:end
call p.bat
