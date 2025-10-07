# utils_xs

Python Utils for the Windows command line requiring minimal set of dependencies. 
A lot of source code was generated using prompts that may be lsited on module comment level

* For use, install using `pip install .`  / `pip install .[dev]` 
* For development install as editable using `python -m pip install -e .`
* Check installation path using `pip list -v`
* Create a Work VENV (best to name it `utils_xs` as well), and do not forget to activate it in VSCode so as to get rid off import errors

# Path Structure and Definition via `myenv.bat`

Ensure in Windows to extend Windows `Path` Variable by the path [`bat`](bat), so you are able to call the scripts directly

Use the copy/paste template [`templates/myenv_template.bat`](templates/myenv_template.bat) and copy it as `myenv.bat` to [`bat`](bat) folder and adjust the variables as needed. This will define locations where scripts will look for scripts and files and paths. 

Run [`bat/bat2py.bat`](bat/bat2py.bat) to transform `colors` and `myenv` definitions in bat files into python files. That way you need to define these variables only once.

Even as you might change path structure it is recommended to stick to predefined work structure as in [`myenv_template.bat`](templates/myenv_template.bat), so that things work together seamlessly. Program Code will be assumed to be stored in a central path, the same goes for stored VENVs. In case repo and VENV name are identical, this can be used to automatically activate VENVs by means of the repo parent folder name ([`bat/va.bat`](bat/va.bat))

As python keeps its Environment within its runtime environment, there's a trick: Python will communicate with the command line via export files containing command snippets or path information. These file snippets will be centrally collected in a path.

# BAT Scripts

* run `bat_list.bat` to list all available vat scripts and a one line documentation
* run `bat_s.bat` to search for available bat scripts by keywords (multiple keyword can be using `ALL` separator `;` and `ANY` separator `:` in a search string)

# TODO
* 🟨 `20251006` Create a JSON from Python Constants Code 
* 🟨 `20251006` Create a markdown toc summary function (`20251006`) 
* 🟨 `20251006` Create shortcuts for frequently used `Git`, `Pip` and `VENV` commands
* 🟨 `20251006` Create shortcut to total commander
* 🟨 `20251007` Use Image Magick to create Thumbnails in SML 
* 🟨 `20251007` Add logic to extract locations 

# DONE

* ✅ `20251006` ~~Script: Move Image files according to their date of creation into new folders using exiftool command~~  
     ~~`exiftool -r -g -json . > metadata.json` (20251005)~~ [`image_organizer.py`](src/scripts/image_organizer.py)

