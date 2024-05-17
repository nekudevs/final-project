import speech_recognition as sr
import pygame
from openai import OpenAI
import requests

client = OpenAI()

def record_audio():
    recognizer = sr.Recognizer()  # Initialize recognizer
    with sr.Microphone() as source:
        print("Speak Now...")
        audio = recognizer.listen(source)  # Listen for audio
    return audio

def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
            #hello_spot(options)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are the best voice assistant, skilled in explaining complex concepts with great accuracy and ease of understanding."},
                {"role": "user", "content": text}
            ]
        )
        print(completion.choices[0].message.content)
        return str(completion.choices[0].message.content)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None
    
def listen_for_stop_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'stop' to stop playback.")
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            if 'stop' in text.lower():
                return True
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return False

def write_to_file(text):
    with open("recognized_text.txt", "w") as file:
        file.write(text)
        print("Speech saved to recognized_text.txt")

def play_mp3(file_path):
    # Initialize the pygame mixer
    pygame.mixer.init()
    
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    
    # Play the MP3 file
    pygame.mixer.music.play()
    
    # Keep the script running until the music stops playing
    while pygame.mixer.music.get_busy():
        if listen_for_stop_command():
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10) # Check every 10 milliseconds


if __name__ == "__main__":
    recorded_audio = record_audio()
    recognized_text = recognize_speech(recorded_audio)
    if recognized_text:
        write_to_file(recognized_text)

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/XB0fDUnXU5powFXDhCwa"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "6e9c90671d01ef2f1a993b7b730ba474"
    }

    data = {
    "text": recognized_text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    play_mp3('output.mp3')
