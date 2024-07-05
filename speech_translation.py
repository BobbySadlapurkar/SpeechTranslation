import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os

def main():
    recognizer = sr.Recognizer()
    translator = Translator()

    while True:
        with sr.Microphone() as source:
            print("Speak Now: ")
            audio = recognizer.listen(source)

            try:
                speech_text = recognizer.recognize_google(audio)
                print(f"You said: {speech_text}")

                if speech_text.lower() == "exit":
                    print("Exiting...")
                    break

                translated_text = translator.translate(speech_text, dest='hi').text
                print(f"Translated to Hindi: {translated_text}")

                voice = gTTS(translated_text, lang='hi')
                voice.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")

            except sr.UnknownValueError:
                print("Could not understand the audio. Please try again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service; check your network connection.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
