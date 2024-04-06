import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import pyaudio
from textblob import TextBlob
from autocorrect import Speller 

# Initialize recognizers and engine
recognizer = sr.Recognizer()
translator = Translator()
engine = pyttsx3.init()
spell = Speller()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def online_voice_typing():
    with sr.Microphone(device_index=0) as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        recognized_text = recognizer.recognize_google(audio, language="auto")
        print("You said:", recognized_text)
        speak("You said: " + recognized_text)  # Auditory feedback

        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        speak("Sorry, could not understand audio.")  # Auditory feedback
        return ""
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        speak("Error fetching results.")  # Auditory feedback
        return ""
    except Exception as e:
        print("Error:", e)
        speak("An error occurred.")  # Auditory feedback
        return ""

def offline_voice_typing():
    try:
        with sr.AudioFile("offline_audio.wav") as source:
            print("Processing offline audio...")
            audio_data = recognizer.record(source)

        print("Recognizing offline audio...")
        recognized_text = recognizer.recognize_sphinx(audio_data)
        print("You said:", recognized_text)
        speak("You said: " + recognized_text)  # Auditory feedback

        return recognized_text
    except sr.UnknownValueError:
        print("Sorry, could not understand offline audio.")
        speak("Sorry, could not understand offline audio.")  # Auditory feedback
        return ""
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        speak("Error fetching results.")  # Auditory feedback
        return ""
    except Exception as e:
        print("Error:", e)
        speak("An error occurred.")  # Auditory feedback
        return ""

def translate_text(text, dest_language='en'):
    try:
        # Translate the text to the desired language
        translation = translator.translate(text, dest=dest_language)
        print(f"Translated to {dest_language}: {translation.text}")
        speak(f"Translated to {dest_language}: " + translation.text)  # Auditory feedback

        return translation.text
    except Exception as e:
        print("Translation Error:", e)
        speak("Translation Error.")  # Auditory feedback
        return ""

def auto_correct(text):
    corrected_text = spell(text)
    print("Auto-corrected text:", corrected_text)
    speak("Auto-corrected text: " + corrected_text)  # Auditory feedback
    return corrected_text

def manual_correct(text):
    corrected_text = TextBlob(text).correct()
    print("Manually corrected text:", corrected_text)
    speak("Manually corrected text: " + str(corrected_text))  # Auditory feedback
    return str(corrected_text)

def additional_features(text):
    print("Do you want to auto-correct or manually correct the text?")
    speak("Do you want to auto-correct or manually correct the text?")
    print("1. Auto-correct")
    print("2. Manual correction")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        return auto_correct(text)
    elif choice == '2':
        return manual_correct(text)
    else:
        print("Invalid choice. Returning original text.")
        speak("Invalid choice. Returning original text.")
        return text

if __name__ == "__main__":
    # Example usage:
    online_text = online_voice_typing()
    offline_text = offline_voice_typing()
    translated_text = translate_text(online_text)

    # Additional Features
    corrected_text = additional_features(translated_text)
