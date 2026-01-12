
@echo off
rem vas.bat Venv Activate Silent. Only calls va.bat if not Virtual env is activated 

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
rem call setenv.bat

if defined VIRTUAL_ENV ( goto end )
call va.bat %*

:end



