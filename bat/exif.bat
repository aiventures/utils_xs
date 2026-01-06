@echo off
rem exif.bat [files] Shortcut to view images using exiftool -g -j  -c '%.6f   [files] 

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

echo %C_T%### RUN %C_PROG%%~f0%C_PY%

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1
set "files_to_show=*.jpg"
if %NUM_ARGS% EQU 0 (    
    goto run_exiftool
)
:show_file
set "files_to_show=%1"

:run_exiftool
:: Now run the command saved from python program assumes exiftool is in path
exiftool -g -j -c '%.6f' %* %files_to_show%
set files_to_show=
echo %C_0%
goto end
:end



