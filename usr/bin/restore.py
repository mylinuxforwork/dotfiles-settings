#  __  __ _    _  ___        __                _                 
# |  \/  | |  | || \ \      / /  _ __ ___  ___| |_ ___  _ __ ___ 
# | |\/| | |  | || |\ \ /\ / /  | '__/ _ \/ __| __/ _ \| '__/ _ \
# | |  | | |__|__   _\ V  V /   | | |  __/\__ \ || (_) | | |  __/
# |_|  |_|_____| |_|  \_/\_/    |_|  \___||___/\__\___/|_|  \___|
#                                                                

import sys
import subprocess
import os
import json
import pathlib
import shutil

# Get script path
pathname = os.path.dirname(sys.argv[0])

class ML4WRestore:

    waybar_themes = [
        "ml4w-minimal",
        "ml4w",
        "ml4w-blur",
        "ml4w-blur-bottom",
        "ml4w-bottom"
    ]

    path_name = pathname # Path of Application
    homeFolder = os.path.expanduser('~') # Path to home folder
    dotfiles = homeFolder + "/dotfiles/"
    settings = {}
    version = sys.argv[1]

    def __init__(self):
        print(":: ML4W Restore")
        print(self.version)
               
        # Load settings.json
        settings_file = open(self.dotfiles + ".settings/settings.json")
        settings_arr = json.load(settings_file)
        for row in settings_arr:
            self.settings[row["key"]] = row["value"]

        # print(self.settings)

        # Waybar Network
        if "waybar_network" in self.settings:
            if self.settings["waybar_network"]:
                print("true")
            else:
                print("false")
            print (":: waybar_network restored")

        # Waybar ChatGIT
        if "waybar_chatgpt" in self.settings:
            if self.settings["waybar_chatgpt"]:
                print("true")
            else:
                print("false")
            print (":: waybar_chatgpt restored")

        # Waybar Network
        if "waybar_systray" in self.settings:
            if self.settings["waybar_systray"]:
                print("true")
            else:
                print("false")
            print (":: waybar_systray restored")

        # Waybar Network
        if "waybar_screenlock" in self.settings:
            if self.settings["waybar_screenlock"]:
                print("true")
            else:
                print("false")
            print (":: waybar_screenlock restored")

        # Waybar Workspaces
        if "waybar_workspaces" in self.settings:
            print(self.settings["waybar_workspaces"])
            print (":: waybar_workspaces restored")

        # Rofi BorderSize
        if "rofi_bordersize" in self.settings:
            print(self.settings["rofi_bordersize"])
            print (":: rofi_bordersize restored")

    # Overwrite Text in File
    def overwriteFile(self, f, text):
        file=open(self.dotfiles + f,"w+")
        file.write(text)
        file.close()

    # Replace Text in File
    def replaceInFile(self, f, search, replace):
        file = open(self.dotfiles + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        # Strips the newline character
        for l in lines:
            count += 1
            if search in l:
                found = count
        if found > 0:
            lines[found - 1] = replace + "\n"
            with open(self.dotfiles + f, 'w') as file:
                file.writelines(lines)

    # Replace Text in File
    def replaceInFileNext(self, f, search, replace):
        file = open(self.dotfiles + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        # Strips the newline character
        for l in lines:
            count += 1
            if search in l:
                found = count
        if found > 0:
            lines[found] = replace + "\n"
            with open(self.dotfiles + f, 'w') as file:
                file.writelines(lines)


ml4wrestore = ML4WRestore()
