import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os

# Define supported languages
supported_languages = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    # Add more languages as needed
}

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()


def detect_language(text):
    # Use Google Translate to detect the language of the input text
    detected_language = translator.detect(text).lang
    return detected_language


def choose_language(source_language):
    # Prompt user to choose target language
    print("Select the language you want to translate to:")

    # Display supported languages
    for code, name in supported_languages.items():
        if code != source_language:
            print(f"\t({code}) {name}")

    # Get user input and validate
    while True:
        chosen_language = input("Enter your choice: ").lower()

        if chosen_language in supported_languages:
            if chosen_language != source_language:
                return chosen_language
            else:
                print("Please choose a different language.")
        else:
            print("Invalid choice. Please enter a valid language code.")


# Loop continuously
while True:
    # Get user input
    print("Speak your sentence:")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    # Try to recognize the speech
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        continue
    except sr.RequestError:
        print("There was an error connecting to the Google Speech Recognition service.")
        continue

    # Detect source language
    source_language = detect_language(text)
    print(f"Detected language: {supported_languages.get(source_language, 'Unknown')}")

    # Determine target language
    target_language = choose_language(source_language)

    # Translate the text
    translated_text = translator.translate(text, dest=target_language).text
    print("Translation:", translated_text)

    # Convert text to speech
    voice = gTTS(translated_text, lang=target_language)
    voice.save("voice.mp3")

    # Play the translated audio
    playsound("voice.mp3")
    os.remove("voice.mp3")

    # Exit if user wants to
    if input("Type 'exit' to stop or press Enter to continue: ").strip().lower() == 'exit':
        break

