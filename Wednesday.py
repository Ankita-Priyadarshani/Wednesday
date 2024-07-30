import time
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import sys
import requests
import pyautogui
import psutil

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning! Hi, I am Jarvis. Please tell me how may I help you!")
    elif 12 <= hour < 18:
        speak("Good Afternoon! Hi, I am Jarvis. Please tell me how may I help you!")
    else:
        speak("Good Evening! Hi, I am Jarvis. Please tell me how may I help you!")
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time right now is {strTime}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception:
            speak("Say that again please... I can't hear you.")
            return "None"
        return query.lower()

def executeTask(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    elif 'who am i' in query:
        speak("You are admin and creator.")
    elif 'who are you' in query:
        speak("I am Wednesday, your own AI.")
   
    elif 'take screenshot' in query:
        speak("Sir, please tell me the name for this screenshot file.")
        name = takeCommand()
        speak("Please hold the screen for a few seconds, I am taking a screenshot.")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        speak("I am done, sir. The screenshot is saved in our main folder. Now I am ready for the next one.")
    elif 'open facebook' in query:
        speak("Opening Facebook for you.")
        webbrowser.open("facebook.com")
    elif 'open youtube' in query:
        speak("Opening YouTube for you.")
        webbrowser.open("youtube.com")
    elif 'open google' in query:
        speak("Opening Google for you.")
        speak("Sir, what should I search for you on Google?")
        cm = takeCommand()
        webbrowser.open(f"{cm}")
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time right now is {strTime}.")
    elif 'open cmd' in query:
        speak("Opening CMD for you, sir.")
        os.system("start cmd")
    elif 'Wednesday' in query:
        speak("What is the order for me, sir?")
    elif 'how much power left' in query or 'battery' in query:
        battery = psutil.sensors_battery()
        percentage = battery.percent
        speak(f"Sir, our system has {percentage} percent battery left.")
        if percentage <= 30:
            speak("It is recommended to plug in the charger.")
        elif percentage <= 50:
            speak("I recommend you to plug in the charger, but as you wish, sir.")
        elif percentage >= 80:
            speak("Sir, the system is ready to use. No need to charge it now.")
    elif 'shut down' in query or 'exit' in query or 'sleep' in query:
        speak("Thanks for using me, sir. Have a good day.")
        sys.exit()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        if query != "None":
            executeTask(query)