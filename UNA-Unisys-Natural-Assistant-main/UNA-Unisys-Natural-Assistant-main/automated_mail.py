import speech_recognition as sr
import time
import smtplib

from fuzzywuzzy import process

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import os
#os.chdir(r"C:\Users\Chinmay\Downloads\new")
#print(os.getcwd())

sender = '1ms18cs036@gmail.com'
EMAIL_PASSWORD = 'INCORRECT19'
receivers = []
more_users = 1
break_ = 0

mail_ids = { "Dheeraj Bhat": "bhatdheeraj19@gmail.com", "Aravind Shreyas Ramesh" : "aravindshreyasramesh@gmail.com", "Gaurav Vinay" : "gv71.msrit@gmail.com", "Chinmay Bhatkal": "chinmay.bhatkal@gmail.com"}
users = ["Aravind Shreyas Ramesh", "Chinmay Bhatkal", "Gaurav Vinay","Dheeraj Bhat"]


def get_subject():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Subject of the Mail')
        audio = r.listen(source)
        #time.sleep(1)
        try:
            text = r.recognize_google(audio)
            print(text)
            return(text)
        except:
            print('Could not recognize your voice! Try again')
            return(get_subject())


def get_mail():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Actual Mail')
        audio = r.listen(source)
        #time.sleep(1)
        try:
            text = r.recognize_google(audio)
            print(text)
            return(text)
        except:
            print('Could not recognize your voice! Try again')
            return(get_mail())


def get_user_id(text):
    return mail_ids[text]

from fuzzywuzzy import process
def find_user(user, users):
    highest = process.extractOne(user, users)
    return(get_user_id(highest[0]))


def get_receiver():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Receiver Mail Address')
        audio = r.listen(source)
        #time.sleep(1)
        try:
            text = r.recognize_google(audio)
            text = find_user(text, users)
            print(text)
            return(text)
        except:
            print('Could not recognize your voice! Try again')
            return(get_receiver())


def get_receivers():
    global more_users
    global break_
    while True:
        if(more_users == 1):
            receiver = get_receiver()
            receivers.append(receiver)
            more_users = 0
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('More users?')
            audio = r.listen(source)
            #time.sleep(1)
            try:
                text = r.recognize_google(audio)
                if(text != "no"):
                    more_users = 1
                    get_receivers()
                else:
                    print("Done")
                    break_ = 1
                    return
            except:
                print('Could not recognize your voice! Try again')
                get_receivers()
        if(break_ == 1):
            break

def find_similar(word, words):
    highest = process.extractOne(word, words)
    return(highest[0])


def receive_attachment():
    r1 = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak the file name")
        audio1 = r1.listen(source)
        #time.sleep(1)
        try:
            text1 = r1.recognize_google(audio1)
            files = os.listdir()
            filename = find_similar(text1, files)
            print(filename)
            
            with open(os.getcwd()+ "\\" + filename , "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)
        except:
            print('Could not recognize your voice! Try again')
            return(receive_attachment())



def attachments():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Has attachment?')
        audio = r.listen(source)
        # #time.sleep(1)
        try:
            text = r.recognize_google(audio)
            text = text.lower()
            if(text != "no"):
                receive_attachment()
        except:
            print('Could not recognize your voice! Try again')
            attachments()


if __name__ =="__main__":
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