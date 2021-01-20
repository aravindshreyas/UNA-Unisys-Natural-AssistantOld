import sys
import os
import pyttsx3
import speech_recognition as sr

import wikipedia
import webbrowser


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from gui import Ui_unaUI

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# tts


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.date.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning !")
    elif hour > 12 and hour < 18:
        speak("Good afternoon !")
    else:
        speak("Good Evening")
    speak("I'm here to help ! Ask me anything")


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening ...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
        try:
            print("Recognizing ...")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said : {query}")

        except Exception as e:
            speak("Say that again ")
            return "none"
        return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takeCommand().lower()
            if "wikipedia" in self.query:
                speak("Searching wikipedia")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak(results)
                print(results)

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_unaUI()
        self.ui.setupUi(self)
        startExecution.start()


app = QApplication(sys.argv)
una = Main()
una.show()
exit(app.exec_())
