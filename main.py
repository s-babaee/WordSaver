import csv
import keyboard
import pyperclip
from deep_translator import GoogleTranslator
from plyer import notification
import requests
import time

FILENAME = "words.csv"
SHORTCUT_SAVE_AND_TRANSLATE = "z+0"  # for auto save and translate
SHORTCUT_KEY = "z+1"  # Shortcut key to save the copied word
SHORTCUT_KEY1 = "z+2"  # for auto_complete_meanings

# Function to get synonyms from Datamuse API
def get_synonyms(word):
    url = f"https://api.datamuse.com/words?rel_syn={word}"
    response = requests.get(url)
    synonyms = [item['word'] for item in response.json()]
    return synonyms

# Function to get antonyms from Datamuse API
def get_antonyms(word):
    url = f"https://api.datamuse.com/words?rel_ant={word}"
    response = requests.get(url)
    antonyms = [item['word'] for item in response.json()]
    return antonyms

# Initialize the CSV file
def initialize_file():
    try:
        with open(FILENAME, 'x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Word", "Meaning", "Synonyms", "Antonyms", "Example", "Count"])  # Adding column headers
    except FileExistsError:
        pass  # No need to create the file again if it already exists

# Add a word to the CSV file
def add_word(word):
    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            words = {row[0] for row in reader}  
    except FileNotFoundError:
        words = set()  

    if word in words:
        print(f"⚠️ '{word}' already exists in the file!\n")
        show_notification(f"⚠️ '{word}' already exists in the file!")
        return  

    # add new word to DB
    with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([word, "", "", "", "", 0])  
    print(f"✅ '{word}' has been successfully saved!\n")
    show_notification(f"✅ '{word}' has been successfully saved!\n")

# Display stored words
def show_words():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            words = list(reader)
            if len(words) > 1:
                print("\n📖 Stored word list:\n")
                for i, (word, meaning, synonyms, antonyms, example, count) in enumerate(words[1:], 1):
                    print(f"{i}. {word} - {meaning if meaning else '🔹 (No meaning)'} | Synonyms: {synonyms if synonyms else 'N/A'} | Antonyms: {antonyms if antonyms else 'N/A'} | Example: {example if example else 'N/A'}")
            else:
                print("❌ No words have been saved yet.\n")
    except FileNotFoundError:
        print("❌ Words file not found!\n")

# Function that runs when the shortcut is pressed
def on_shortcut():
    word = pyperclip.paste().strip()  # Read text from clipboard
    if word:
        add_word(word)
    else:
        print("⚠️ No word found in the clipboard!")
        show_notification("⚠️ No word found in the clipboard!")

# Get translation, synonyms, antonyms, and example
def get_word_info(word):
    """Fetch translation, synonyms, antonyms, and example sentences for a word."""
    translation = GoogleTranslator(source='en', target='fa').translate(word)

    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)

    return {
        "translation": translation,
        "synonyms": ", ".join(synonyms) if synonyms else "N/A",
        "antonyms": ", ".join(antonyms) if antonyms else "N/A",
        "example": "N/A"  # Still not using example for now
    }

# Auto-complete meanings and update the CSV file
def auto_complete_meanings():
    """Update the CSV file with translations, synonyms, antonyms, and example sentences."""
    try:
        with open(FILENAME, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            words = list(reader)

        updated = False

        # Update words that have missing meanings
        for i in range(1, len(words)):  # Start from index 1 (skip headers)
            word_row = words[i] + [''] * (6 - len(words[i]))  # Add empty values if not enough columns
            word, meaning, synonyms, antonyms, example, count = word_row

            if not meaning.strip():  # If meaning is empty
                info = get_word_info(word)
                words[i] = [
                    word,
                    info["translation"],
                    info["synonyms"],
                    info["antonyms"],
                    info["example"],
                    0  # Set the initial count to 0
                ]
                updated = True
                print(
                    f"✅ '{word}' → '{info['translation']}' | Synonyms: {info['synonyms']} | Antonyms: {info['antonyms']}")

        if updated:
            with open(FILENAME, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerows(words)  # Save updated data
            print("\n✅ Word meanings updated successfully!\n")
            show_notification("✅ Word meanings updated successfully!\n")
        else:
            print("\n🔹 All words already have meanings.\n")
            show_notification("🔹 All words already have meanings.\n")

    except FileNotFoundError:
        print("❌ Words file not found!\n")
        show_notification("❌ Words file not found!\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        show_notification("❌ Error: ")

# Show notification
def show_notification(message):
    notification.notify(
        title='Word Saver',
        message=message,
        timeout=2
    )

def save_and_translate():
    on_shortcut()
    auto_complete_meanings()

# Run the program
def main():
    initialize_file()
    print(f"📌 The program is running... Copy any word and press '{SHORTCUT_SAVE_AND_TRANSLATE}' to save and translate it.")
    print("🛑 Press 'Ctrl+C' to exit.")

    keyboard.add_hotkey(SHORTCUT_KEY, on_shortcut)
    keyboard.add_hotkey(SHORTCUT_KEY1, auto_complete_meanings)
    keyboard.add_hotkey(SHORTCUT_SAVE_AND_TRANSLATE, save_and_translate)
    keyboard.wait()  # Keep the program running

if __name__ == "__main__":
    main()
