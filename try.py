import os
import sys
import wave
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def hotword():
    model_path = "D:/python projects/model_path"  # Path to the Vosk model directory
    if not os.path.exists(model_path):
        print(f"Model path does not exist: {model_path}")
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
                    detected_text = result["text"].strip().lower()
                    print(f"Detected text: {detected_text}")
                    if detected_text == "iris":
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

# Call the hotword function
hotword()
