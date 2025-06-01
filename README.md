# WordSaver

**WordSaver** is a Python program that lets you quickly save and translate words you copy, fetch their synonyms and antonyms, and store all the data in a CSV file.

---

## Features

- Automatically save copied words using shortcut keys  
- Translate words from English to Persian  
- Retrieve synonyms and antonyms using the free Datamuse API  
- Show desktop notifications on save or error  
- Store words, translations, synonyms, antonyms, examples, and counts in a `words.csv` file

---

## Requirements

- Python 3.6 or higher  
- Python packages (install with pip):  
  - `keyboard`  
  - `pyperclip`  
  - `deep_translator`  
  - `plyer`  
  - `requests`  

Install all dependencies with:

```bash
pip install keyboard pyperclip deep_translator plyer requests

# Run the program
Simply double-click the included run_script.bat file or run it from the command line.

# How to use
- Copy any English word to your clipboard (Ctrl+C)
- Use these shortcut keys inside the program:

| Shortcut  | Action                       |
|-----------|------------------------------|
| `z + 1`   | Save the copied word          |
| `z + 2`   | Auto-complete meanings and data |
| `z + 0`   | Save and auto-complete together |
