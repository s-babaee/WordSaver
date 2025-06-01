# WordSaver

**WordSaver** is a Python program that lets you quickly save and translate words you copy, and fetch their synonyms and antonyms, storing all data in a CSV file.

---

## Features

- Save copied words automatically using shortcut keys  
- Translate words from English to Persian  
- Get synonyms and antonyms using the free Datamuse API  
- Show desktop notifications on save or error  
- Store words, translations, synonyms, antonyms, and examples in a `words.csv` file

---

## Requirements

You need:

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

How to Run
Just run the included run_script.bat file by double-clicking it or running it from the command line. This will start the program with the correct Python environment.

When running:

Copy any English word to your clipboard (Ctrl+C)

Use these shortcut keys inside the program:

Shortcut	Action
z+1	Save the copied word
z+2	Auto-complete meanings and data
z+0	Save and auto-complete together

CSV File Format
The words.csv file stores data in columns:

| Word | Meaning | Synonyms | Antonyms | Example | Count |

Notes
Make sure you have an active internet connection for translations and synonyms

You can customize shortcut keys in the source code if needed

Desktop notifications inform you about success or errors