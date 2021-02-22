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
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup 
import kivy

from automated_mail import *

kivy.require('2.0.0')  # replace with your current kivy version !

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)



reminder_text = ""
date_text = ""


class PopupLayout(GridLayout):
    def __init__(self, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)

        self.cols = 1
        self.row_force_default = True
        self.row_default_height = 120
        self.col_force_default = True
        self.col_default_width = 100

        #create a second gridlayout 
        self.top_grid = GridLayout(
                row_force_default = True,
                row_default_height = 40,
                col_force_default = True,
                col_default_width = 200
                )
        self.top_grid.cols = 2

        self.top_grid.add_widget(Label(text="Reminder: "))
        self.reminder = TextInput(multiline=False)
        self.top_grid.add_widget(self.reminder)

        self.top_grid.add_widget(Label(text="Date(yyyy/mm/dd) : "))
        self.date= TextInput(multiline=False)
        self.top_grid.add_widget(self.date)

        #add new grid
        self.add_widget(self.top_grid)

        #create submit button
        self.submit = Button(text="Submit",
            font_size= 32,
            size_hint_y = None,
            height = 50,
            size_hint_x = None,
            width = 200
         )
        self.submit.bind(on_press = self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        reminder_text = self.reminder.text
        date_text = self.date.text

        
        self.reminder.text = ''
        self.data.text = ''

class MyLayout(Widget):
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
                print("Error")
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
            # self.add_widget(Label(text=f"Name:{results}"))
            # self.ids.listens.text = "results"
            self.speak(results)
            #self.ids.listens.text = 'Listen'
            
        elif "open youtube" in command:
            webbrowser.open("www.youtube.com")

        elif "mail" in command:
            subject = get_subject()
            mail = get_mail()
            get_receivers()

            receivers_string = ",".join(str(x) for x in receivers)
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = receivers_string
            text = MIMEText(mail, "plain")
            message.attach(text)
            attachments()
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender, EMAIL_PASSWORD)
                    smtp.sendmail(sender, receivers, message.as_string())
                    print("Done")
            except Exception as e:
                print(e)

        elif "directory" in command:
            print(os.getcwd())

        elif "set reminder" in command:
            MyPopup().open()

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour <= 12:
            self.speak("Good morning !")
        elif hour > 12 and hour < 18:
            self.speak("Good afternoon !")
        else:
            self.speak("Good Evening")
        self.speak("I'm here to help ! Ask me anything")


    def hello(self):
        pass
        # self.add_widget(Label(text=f"Name:bye"))
        #self.speak("Hello")

class unaApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    #unaApp().run()
    popup = Popup(title='Test popup',
    content=Label(text="hello!"),
    auto_dismiss= False)
    popup.open()


