@echo off 
rem video_remame.bat renaming videos in current file and subfolders and consolidating video descriptions into a json 

rem activate variables and virtuakl environment 
call setenv.bat

@REM if not defined MY_P_MYENV (
@REM     echo %C_E%Path MY_P_MYENV to store variables is not defined%C_0%
@REM     goto end
@REM )

if not defined MY_P_UTILS_SCRIPTS (
    echo %C_E%Path MY_P_UTILS_SCRIPTS containing scripts is not defined%C_0%
    goto end
)

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

rem save the environment variable
set "py_prog=%MY_P_UTILS_SCRIPTS%\video_rename.py"
python %py_prog% %*

:end
echo %C_0%


