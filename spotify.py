import speech_recognition as sr
import pyaudio
import pyttsx3
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ollama


load_dotenv()
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')


if not client_id or not client_secret or not redirect_uri:
    raise ValueError("Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI environment variables.")


scope = 'user-read-private user-read-email user-top-read user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                            client_secret=client_secret,
                                            redirect_uri=redirect_uri,
                                            scope=scope))






def skip_track(response):
    if response == "SKIP":
        try:
            sp.next_track()
        except spotipy.exceptions.SpotifyException:
            print("Couldn't Skip")
    elif response == "PAUSE":
        try:
            pause_track()
        except spotipy.exceptions.SpotifyException:
            print("Couldn't Pause")
    elif response == "PLAY":
        try:
            play_track()
        except spotipy.exceptions.SpotifyException:
            print("Couldn't Play")



def pause_track():
    sp.pause_playback()
    print("Paused the track.")


def play_track():
   sp.start_playback()
   print("Resumed Track")


def test(input):
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f"Respond with a 'SKIP' if the input shows that the song should be skipped. If the song should be paused or the music needs to be stopped, respond with 'PAUSE'. If the music should be started, then have a response of 'PLAY' to restart the playback. If none of these should happen, respond with FALSE. Your response should either be SKIP, PAUSE, PLAY, or FALSE \n{input}",
        },
    ])
    response = response['message']['content']
    print(response)
    skip_track(response)

recognizer = sr.Recognizer()
while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"Recognized {text}")
            test(text)
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        continue
