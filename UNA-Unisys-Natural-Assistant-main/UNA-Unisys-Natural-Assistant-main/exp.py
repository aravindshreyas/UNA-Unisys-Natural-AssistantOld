import datetime
import webbrowser
import wikipedia

import speech_recognition as sr
from pyttsx3.engine import Engine
import pyttsx3

import os
import sys
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

if __name__ == '__main__':
    message = "hello world!"
    print(message)
    engine.say(message)
    engine.runAndWait()
    engine.stop()


