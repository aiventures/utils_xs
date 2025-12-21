@echo off
rem venv_create.bat [venv_name|optional] create a venv with a venv_name (or enter from prompt)

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

set pwd=%CD%
set num_args=0

:: Count number of arguments
for %%x in (%*) do set /A num_args+=1
rem Handle missing arguments
if %num_args% equ 0 (
    echo %C_T%No venv name supplied.%C_0%
    set /p venv_name=%C_Q%Please enter venv name^>%C_0% 
) else (
    set venv_name=%~1
)

echo %C_T%Creating virtual environment %C_I%%venv_name%%C_P% (%MY_P_VENV%)%C_0% 
cd %MY_P_VENV%

rem Example: create the virtual environment
if not exist "%venv_name%" (    
    echo Creating virtual environment folder "%venv_name%"...
    python -m venv "%venv_name%"
) else (
    echo Virtual environment "%venv_name%" already exists.
)

goto end
:end
cd %pwd%
set num_args=
set pwd=
set venv_name=
echo %C_0%

