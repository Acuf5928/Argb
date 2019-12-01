#!/usr/bin/env python3
import time
import _thread

from gui_trayicon import main as gui
from code_data import data

#avvio interfaccia grafica
while True:
    gui("img_whiteicon.png", data)
    