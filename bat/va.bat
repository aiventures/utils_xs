
@echo off
rem va.bat [venv_name|optional] - activates VENV from %MY_P_VENV%, checks parent path match, or defaults to %MY_P_VENV_WORK%

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

rem check if there is already a venv if so do nothing
rem if defined VIRTUAL_ENV (
rem   echo %C_W%There is already an activated VIRTUAL_ENV %VIRTUAL_ENV%, deactivate first  %C_0%
rem   goto end
rem )
rem last used folder name 
for %%A in ("%cd%") do set MY_LAST_FOLDERNAME=%%~nxA
rem echo %CURRENT_FOLDER%
set venv_name=

:: Count arguments
set pwd=%CD%
set num_args=0
for %%x in (%*) do set /A num_args+=1

:: Extract current parent folder name
for %%I in ("%CD%") do set "parent_path=%%~nI"
:: assume there is venv and work repo at current location
set "venv_path=%MY_P_VENV%\%parent_path%"
set "venv_name=%parent_path%"

:: If no parameter is passed
if "%~1"=="" (
    echo %C_T%No venv_name provided.%C_0%
    if exist "%venv_path%\Scripts\activate.bat" (
        echo %C_T%Found matching venv for parent folder: %C_P%%parent_path%
        if defined VIRTUAL_ENV (
            echo %C_PY%Deactivating current venv: %C_P%%VIRTUAL_ENV%
            call deactivate
            call p.bat
        )
        call "%venv_path%\Scripts\activate.bat"
        call p.bat
        echo %C_0%
        goto change_path
    )

    :: If not found, activate default venv if not already done
    rem echo hugo _%MY_VENV%_ _%MY_VENV_DEFAULT%_ 
    if defined MY_VENV if /i "%MY_VENV%"=="%MY_VENV_DEFAULT%" (
        echo %C_I%Default Environment %MY_VENV_DEFAULT% already set%C_=%
        goto end
    )

    echo %C_T%Activating default: %C_P%%MY_P_VENV_WORK%
    if defined VIRTUAL_ENV (
        echo %C_W%Deactivating current venv: %C_P%%VIRTUAL_ENV%
        call deactivate
        call p.bat
    )
    call "%MY_P_VENV_WORK%\Scripts\activate.bat"
    call p.bat
    echo %C_0%
    goto change_path
)

:: If param is given, try to activate from VENV Name
rem %~1 removes outer paragraphs
set "venv_name=%~1"
set "venv_path=%MY_P_VENV%\%venv_name%"

rem skip if the venv is already the same 
if not defined MY_VENV ( goto after_check_for_same_venv )

if /i "%MY_VENV%"=="%venv_name%" ( 
    echo %C_W%Venv %venv_name% already activated%C_0%
    goto end
) 

:after_check_for_same_venv

if exist "%venv_path%\Scripts\activate.bat" (
    if defined VIRTUAL_ENV (
        echo %C_PY%Deactivating current venv: %C_P%%VIRTUAL_ENV%
        call deactivate
        call p.bat
    )
    echo %C_PY%Activating virtual environment: %C_P%%venv_path%
    call "%venv_path%\Scripts\activate.bat"    
    call p.bat
) else (
    echo %C_E%ERROR: Virtual environment not found at %C_P%%venv_path%
)
echo %C_0%
goto change_path

:change_path
set "repo_path=%MY_P_REPO%\%venv_name%"

if exist %repo_path% (
  echo %C_T%Found corresponding repo path , navigate to %C_P%%repo_path%%C_0%
  cd %repo_path%
  set /p back=%C_Q%Navigate back to original path %C_P%[%pwd%]%C_Q% ^(y^) ^>

  if "%back%"=="y" ( cd %pwd% )
) else (
  echo %C_T%No repo path derived, use last path %C_P%%pwd%%C_0%
  cd %pwd%
)

set pwd=
set venv_name=
set venv_path=
set num_args=
set venv_auto_path=
set repo_path=
rem set the last virtual env path
set MY_VENV=
if not defined VIRTUAL_ENV ( goto end ) 
:set_venv_name
for %%A in ("%VIRTUAL_ENV%") do set MY_VENV=%%~nxA
:end
call p.bat
