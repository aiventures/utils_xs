# 🐍 Summary: `bat_list.py`

A modular Python script for searching, displaying, and executing `.bat` files with interactive input and ANSI-colored output.

---

## 🔧 Features

- **Batch File Discovery**  
  - Scans one or more directories for `.bat` files.
  - Builds a dictionary with index, absolute path, and description.

- **Description Extraction**  
  - Reads the first `REM` comment from each file (case-insensitive).
  - If none found, assigns `"no text found"`.

- **ANSI Color Output**  
  - Uses predefined color codes for titles, indices, search terms, highlights, errors, etc.
  - Example: `f"{C_T}Title{C_0}"` for blue title text.

- **Search Functionality**  
  - `:` → ALL terms must be present (AND).
  - `;` → ANY term may be present (OR).
  - Single term → fuzzy match.
  - Highlights matched terms in output.

- **Interactive Selection**  
  - Prompts user to choose a script by index.
  - Parses `[param]` blocks in descriptions.
  - Differentiates required vs. optional/default parameters.
  - Constructs a `call` command and writes it to a file.

- **CLI Integration**  
  - Uses `argparse` for paths, query terms, and output file.
  - Defaults defined via `P_BAT_DEFAULT` and `F_CMD_DEFAULT`.

---

## 📦 Core Functions

| Function                     | Purpose                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| `read_bat_files()`          | Collects `.bat` files and metadata                                      |
| `extract_rem_text()`        | Extracts first REM comment line                                         |
| `highlight_text()`          | Highlights search terms in text using ANSI colors                       |
| `filter_dict()`             | Filters files based on query logic                                     |
| `print_bat_dict()`          | Displays formatted list with color and alignment                        |
| `input_command_interactive()` | Prompts user for selection and arguments                              |
| `get_argparser()`           | Builds CLI parser                                                       |
| `main()`                    | Entry point for script execution                                        |

---

## 🧪 Sample Output (truncated)


### PATH C:\scripts
[001] backup.bat     : Start backup [Path] [optional: Mode]
[002] cleanup.bat    : Removes temporary files

# 🧭 Summary: `browser_bookmarks.py`

A Python script that transforms exported browser bookmarks into a richly navigable Markdown document—with emoji heatmaps, floating sidebars, and hierarchical anchors.

---

## 🔧 Core Features

- **📅 Date-Based Organization**
  - Groups links by Year → Month → Day.
  - Each link formatted as:  
    `* [yyyy-mm-dd linktext](url) → FolderPath (domain.com)`

- **📁 Folder Path Extraction**
  - Traverses `<H3>` tags to reconstruct full folder hierarchy.
  - Skips top two levels for cleaner output.

- **📊 Emoji Heatmaps**
  - Frequency-based visual indicators:
    - 🟩 low
    - 🟨 medium
    - 🟥 high
  - Applied to:
    - TOC vertical bars
    - Domain frequency tables
    - Monthly link counts

- **🧭 Floating Sidebar**
  - HTML+CSS sidebar with anchor links to:
    - Table of Contents
    - Domain Statistics
    - Each year section

- **📌 Anchored TOC Generation**
  - Markdown table layout:
    - Rows = years
    - Columns = months
    - Cells = stacked emoji bars + link count + anchor
  - Fixed-width font and padded counts (e.g. `003`)

- **📈 Domain Statistics**
  - Markdown table of domains from last 365 days.
  - Sorted alphabetically.
  - Includes emoji heatmap and clickable domain links.

- **🔗 Anchor Logic**
  - Sanitizes headers for GitHub-flavored Markdown anchors.
  - Adds `[Back to Top](#table-of-contents)` at end of each section.

---

## 📦 Key Functions

| Function                        | Purpose                                                                 |
|--------------------------------|-------------------------------------------------------------------------|
| `extract_links_by_date()`      | Parses HTML and groups links by date and folder path                   |
| `create_markdown()`            | Builds full Markdown output with TOC, domain stats, and link sections  |
| `generate_toc_table_vertical_heatmap()` | Creates vertical emoji TOC table with anchors and counts     |
| `format_domain_table_recent()` | Builds domain frequency table for recent links                         |
| `generate_floating_sidebar()`  | Outputs HTML sidebar for navigation                                     |
| `build_sidebar_anchors()`      | Generates anchor list for sidebar                                       |
| `get_root_domain()`            | Extracts root domain from URL                                           |
| `generate_anchor()`            | Sanitizes header text for Markdown anchors                              |
| `save()`                       | Writes Markdown and JSON files                                          |

---

## 🧪 Sample Output (simplified)

```markdown
# 2025 [042]
## 2025-10 [012]
### 2025-10-05 [004]
* [2025-10-05 Example Site](https://example.com) → Favorites Bar / DevTools (example.com)

# 🕸️ Summary: `browser_history.py`
```

A Python script that parses exported browser history from a CSV file and generates a richly structured Markdown document—with domain stats, date-based grouping, duplicate tracking, and a floating sidebar for navigation.

---

## 🔧 Core Features

- **📄 CSV Parsing**
  - Reads browser history CSV with columns:
    - `DateTime` (ISO format)
    - `NavigatedToUrl`
    - `PageTitle`
  - Converts encoding to UTF-8 (handles UTF-8-BOM).
  - Extracts:
    - `DateTime` → `datetime.datetime` object
    - `url` → full link
    - `base_url` → root domain (stripped of `http`, `www`)
    - `title` → page title

- **📅 Date-Based Grouping**
  - Organizes links by:
    - Year (`# yyyy`)
    - Month (`## yyyy-mm`)
    - Day (`### yyyy-mm-dd`)
  - Displays duplicate links only once per day, with count in brackets.
  - Adds link count to each day header.

- **📊 Domain Statistics**
  - Section: `## Stats By Domain`
    - Markdown table of all domains visited in last 365 days.
    - Includes count, percentage, and clickable domain links.
  - Section: `## Top 100 Domains`
    - Sorted by frequency.
    - Includes cumulative percentage and emoji indicator bars.

- **📌 Table of Contents**
  - One-line TOC showing number of links per month.
  - Displays last 12 months only.

- **🧭 Floating Sidebar**
  - HTML+CSS sidebar with anchor links to:
    - Table of Contents
    - Stats By Domain
    - Top 100 Domains
    - Recent daily sections (`### yyyy-mm-dd`)

- **🔗 Anchor Logic**
  - Sanitizes headers for GitHub-style Markdown anchors.
  - Sidebar links use these anchors for smooth navigation.

---

## 📦 Key Functions

| Function                        | Purpose                                                                 |
|--------------------------------|-------------------------------------------------------------------------|
| `read_csv_history()`           | Parses CSV and extracts structured records                             |
| `generate_toc_summary()`       | Builds one-line TOC for last 12 months                                 |
| `format_domain_table_recent()` | Creates domain stats and top 100 list                                  |
| `create_markdown()`            | Groups links by date and domain, handles duplicates                    |
| `build_sidebar_anchors()`      | Generates anchor list for sidebar                                      |
| `generate_floating_sidebar()`  | Outputs HTML+CSS sidebar                                               |
| `save()`                       | Writes Markdown and JSON output                                        |

---

## 🧪 Sample Output (simplified)

```markdown
# 2025
## 2025-09
### 2025-09-29 (3 links)
* [xyz.com](https://www.xyz.com)
  * [bla vla](https://www.xyz.com) (2)
  * [another page](https://www.xyz.com)

# 🎨 Summary: `convert_bat_colors_to_python.py`
```
A Python utility that converts Windows batch color definitions (`set VAR=VALUE`) into Python constants, with optional ANSI color code visualization.

---

## 🔧 Core Features

- **📁 Batch to Python Conversion**
  - Parses `.bat` files containing `set VAR=VALUE` lines.
  - Converts each variable into a Python f-string constant.
  - Escapes braces to ensure valid f-string syntax.
  - Replaces `%VAR%` references with `{VAR}` for Python interpolation.

- **📄 Metadata Header**
  - Adds a docstring header with:
    - Source path (escaped for safety)
    - Timestamp of generation

- **🖨️ Output Options**
  - If `--output` is provided, saves result to `.py` file.
  - Otherwise, prints generated Python code to stdout.

- **🎨 ANSI Color Table Display**
  - With `--show-codes`, prints a 36×6 grid of ANSI 256-color codes.
  - Each code is shown as:
    - `ESC[38;5;{code}m{code}` followed by reset (`ESC[0m`)

- **🧪 __main__ Block**
  - When run directly, prints all uppercase constants with color preview.
  - Uses `globals()` to extract constants dynamically.

---

## 📦 Key Functions

| Function                  | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| `create_arg_parser()`    | Builds CLI parser with input/output/show options                        |
| `escape_for_fstring()`   | Escapes `{}` for safe f-string generation                               |
| `save_python_module()`   | Writes generated Python code to file                                    |
| `bat_to_python_colors()` | Parses `.bat` file and generates Python constants                       |
| `show_color_codes()`     | Displays ANSI 256-color codes in formatted grid                         |
| `main()`                 | CLI entry point, handles conversion or color display                    |

---

## 🧪 Sample Output (simplified)

```python
""" This file was generated from C:\\scripts\\colors.bat
Date of generation: 2025-10-05 23:49:00 """
ESC = "\033"
C_RED = f"{ESC}[31m"
C_GREEN = f"{ESC}[32m"
...

# 🔄 Summary: `convert_bat_env_to_python.py`
```
A Python script that converts Windows `.bat` environment variable definitions into a Python module—resolving dependencies, preserving comments, and handling type conversion.

---

## 🔧 Core Features

- **📁 Batch to Python Conversion**
  - Parses lines like:
    - `set VAR=value`
    - `set "VAR=value with spaces"`
  - Converts to Python constants:
    - `VAR = r"value"`
    - Auto-converts to `int` or `float` if applicable.

- **💬 Comment Preservation**
  - Converts preceding `rem` lines to Python comments:
    - `rem this is a comment` → `# this is a comment`

- **🔗 Variable Resolution**
  - Resolves `%VAR%` references recursively.
  - Detects and reports circular dependencies.
  - Example:
    ```bat
    set "ROOT=C:\\xyz"
    set "VENV=%ROOT%\\venv"
    ```
    →  
    ```python
    ROOT = r"C:\\xyz"
    VENV = r"C:\\xyz\\venv"
    ```

- **📄 Metadata Header**
  - Adds docstring with:
    - Original `.bat` file path
    - Generation timestamp
    - Escaped backslashes to avoid `\u` issues

- **🖥️ CLI Interface**
  - Uses `argparse`:
    - `--input` or `-i` (default: `myenv.bat`)
    - `--output` or `-o` (default: `myenv.py`)
  - Error messages for unresolved or circular references.

- **🧪 Main Block**
  - Prints all uppercase constants using `pprint` when run directly.

---

## 📦 Key Functions

| Function                  | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| `parse_bat()`            | Parses `.bat` lines and extracts variables + comments                   |
| `resolve_variables()`    | Recursively resolves `%VAR%` references with circular check             |
| `convert_value()`        | Converts values to `int`, `float`, or raw string                        |
| `save_python_module()`   | Writes formatted Python module with header and resolved variables       |
| `bat_to_python()`        | Orchestrates parsing, resolution, and saving                            |
| `main()`                 | CLI entry point with argument parsing                                   |

---

## 🧪 Sample Output (simplified)

```python
""" This module was generated from C:\\scripts\\myenv.bat
Date of generation: 2025-10-05 23:49:00 """

# working path
MY_P_WORK = r"C:\\xyz"

# path containing venvs
MY_P_VENV = r"C:\\xyz\\VENV"

# path containing work venv
MY_P_VENV_WORK = r"C:\\xyz\\VENV\\WORK"

# 🧮 Summary: `prompt.py`
```
A Python script that dynamically generates a Windows Command Line prompt string with contextual information—such as Git branch and active virtual environment—styled using ANSI color codes.

---

## 🔧 Core Features

- **🎨 Colorized Prompt Rendering**
  - Uses ANSI escape codes from `config.colors`:
    - `C_P`, `C_B`, `C_V`, `C_SC0`, `C_SC1`, `C_0`, `C_1`
  - Applies different styles based on context:
    - Reset mode → basic prompt
    - Venv active → `[{venv}]` in `C_V`
    - Git branch → `(branch)` in `C_B`
    - Prompt symbol → `λ` in `C_SC`

- **🔍 Git Branch Detection**
  - Runs `git rev-parse --abbrev-ref HEAD` via `subprocess`.
  - Returns branch name unless in detached `HEAD` state.

- **🐍 Virtual Environment Detection**
  - Checks:
    - `VIRTUAL_ENV` env variable
    - `sys.prefix` vs `sys.base_prefix`
    - `sys.real_prefix` (legacy support)
  - Returns basename of active venv folder.

- **🧵 Prompt Assembly**
  - Combines components into a single string:
    ```python
    [venv] (branch) $P λ
    ```
  - Adjusts colors based on presence of venv and branch.

- **💾 File Output**
  - Saves final prompt string to configured path:
    - `MY_F_MYENV_PROMPT` from `config.myenv`
    - Format: `SET "PROMPT=..."`

- **🖥️ CLI Entry Point**
  - `main()` generates and saves prompt string.
  - Designed for use in `.bat` file generation workflows.

---

## 📦 Key Functions

| Function            | Purpose                                                  |
|---------------------|----------------------------------------------------------|
| `get_git_branch()`  | Returns current Git branch name                          |
| `get_current_venv()`| Detects active virtual environment name                  |
| `create_prompt()`   | Builds prompt string with color and context              |
| `save_prompt()`     | Writes prompt string to file                             |
| `main()`            | CLI entry point                                          |

---

## 🧪 Sample Output (simplified)

```bat
SET "PROMPT=[venv] (main) $P λ"
```


