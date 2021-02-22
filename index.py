import datetime
import webbrowser
import wikipedia

import speech_recognition as sr
from pyttsx3.engine import Engine
import pyttsx3

import os
import sys
import time

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
import kivy
kivy.require('2.0.0')  # replace with your current kivy version !

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


class assistant:
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening')
            audio = r.listen(source)
            time.sleep(1)
            try:
                command = r.recognize_google(audio)
                command = command.lower()
                print(command)
                self.analyzeText(command)
            except:
                print("Sorry I didn't understand that, please try again.")
                self.speak("Sorry I didn't understand that, please try again.")

    def testInput(self):
        com = "wikipedia lion"
        self.analyzeText(com)

    def speak(self, message):
        print(message)
        engine.say(message)
        engine.runAndWait()
        engine.stop()

    def analyzeText(self, command):
        if "wikipedia" in command:
            self.speak("Searching wikipedia")
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            self.speak(results)
            print(results)
        elif "open youtube" in command:
            webbrowser.open("www.youtube.com")

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour <= 12:
            self.speak("Good morning !")
        elif hour > 12 and hour < 18:
            self.speak("Good afternoon !")
        else:
            self.speak("Good Evening")
        self.speak("I'm here to help ! Ask me anything")


class MyLayout(Widget):
    pass
    #una = assistant()
    # una.testInput()
    # una.listen()


class unaApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    unaApp().run()
