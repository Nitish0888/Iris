import os

import eel

from Engine.features import*
from Engine.command import*

def start():
    eel.init("Design")

    playIrissound()

    os.system('start msedge.exe --app="http://localhost:8000/Design.html"')

    eel.start('Design.html',mode=None,host='localhost',block=True)




