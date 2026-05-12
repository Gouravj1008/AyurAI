import os
import winshell

startup = winshell.startup()
path = os.path.join(startup, "Jarvis.lnk")

exe_path = os.path.abspath("Jarvis.exe")

with winshell.shortcut(path) as shortcut:
    shortcut.path = exe_path
    shortcut.description = "Jarvis Assistant"
