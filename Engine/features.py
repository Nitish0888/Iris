import os
from urllib.parse import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from Engine.command import speak
from Engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine

import struct
import time
import pvporcupine
import pyaudio

import os
import sys
import wave
import json
import pyaudio 
from vosk import Model, KaldiRecognizer

from Engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

conn= sqlite3.connect("Iris.db")
cursor = conn.cursor()


@eel.expose
def playIrissound():
    music_dir="Design\\images\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)



def hotword():
    model_path = "D:\python projects\model_path"  # Path to the Vosk model directory
    if not os.path.exists(model_path):
        print(f"{model_path}")
        sys.exit(1)
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    
    paud = pyaudio.PyAudio()
    audio_stream = paud.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=4096)
    
    try:
        while True:
            data = audio_stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:

                    if "iris" in result["text"].lower():
                        print("Hotword 'iris' detected")

                        # Pressing shortcut key win+j
                        import pyautogui as autogui
                        autogui.keyDown("win")
                        autogui.press("j")
                        autogui.keyUp("win")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        audio_stream.close()
        paud.terminate()

def findContact(query):


    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0



def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        iris_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        iris_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        iris_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(iris_message)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)

def sendMessage(message, mobileNo, name):
    from Engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(176, 2189)
    #start chat
    tapEvents(921, 2149)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(445, 588)
    # tap on input
    tapEvents(271, 1270)
    #message
    adbInput(message)
    #send
    tapEvents(949, 1285)
    speak("message send successfully to "+name)