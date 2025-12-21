
@echo off
rem py_convert_colors.bat converts colors from bat to python (convert_bat_colors_to_python.py)

rem create a script setenv.bat (just like \utils_xs\templates\myenv_template.bat )
rem put it into executable PATH and call it setenv.bat
call setenv.bat

set "py_program=%MY_P_UTILS_SCRIPTS%\convert_bat_colors_to_python.py"
echo %C_T%### RUN %C_PROG%%~f0%C_PY%
echo %C_T%Run Python Program %C_PY%%py_program%%C_0%
echo %C_PY%[%MY_F_COLORS_BAT%] ^> [%MY_F_COLORS_PY%] %C_PY%

:: Count number of arguments
set NUM_ARGS=0
for %%x in (%*) do Set /A NUM_ARGS+=1
python "%py_program%" --input "%MY_F_COLORS_BAT%" --output "%MY_F_COLORS_PY%"
:: Now run the command saved from python program

echo %C_O%
cat %MY_F_COLORS_PY%
goto end

:end
echo %C_0%


