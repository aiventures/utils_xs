
@echo off
rem va.bat [venv_name|optional] - activates VENV from %MY_P_VENV%, checks parent path match, or defaults to %MY_P_VENV_WORK%

call colors.bat
call myenv.bat

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

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
        goto end
    )

    :: If not found, activate default venv
    echo %C_T%Activating default: %C_P%%MY_P_VENV_WORK%
    if defined VIRTUAL_ENV (
        echo %C_PY%Deactivating current venv: %C_P%%VIRTUAL_ENV%
        call deactivate
        call p.bat
    )
    call "%MY_P_VENV_WORK%\Scripts\activate.bat"
    call p.bat
    echo %C_0%
    goto end
)

:: If param is given, try to activate from VENV Name
set "venv_name=%~1"
set "venv_path=%MY_P_VENV%\%venv_name%"

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
goto end

:end
set "repo_path=%MY_P_REPO%\%venv_name%"

if exist %repo_path% (
  echo %C_T%Found corresponding repo path , navigate to %C_P%%repo_path%%C_0%
  cd %repo_path%
  set /p back=%C_Q%Navigate back to original path %C_P%[%pwd%]%C_Q% ^(y^) ^>

  if "%back%"=="y" ( cd %pwd% )
) else (
  echo %C_T%No repo path derived, navigate to %C_P%%pwd%%C_0%
  cd %pwd%
)
set pwd=
set venv_name=
set venv_path=
set num_args=
set venv_auto_path=
set repo_path=
