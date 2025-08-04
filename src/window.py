# window.py
#
# Copyright 2025 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
import sys
import gi
import subprocess
import os
import threading
import json
import pathlib
import shutil
import shlex
import time

@Gtk.Template(resource_path='/com/ml4w/settings/window.ui')
class DotfilesSettingsWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'Ml4wSettingsWindow'

    # Get script path
    pathname = os.path.dirname(sys.argv[0])

    path_name = pathname # Path of Application
    homeFolder = os.path.expanduser('~') # Path to home folder
    dotfiles = homeFolder + "/.config/"

    settings = {
        "waybar_timeformat": "%H:%M",
        "waybar_dateformat": "%a",
        "waybar_custom_timedateformat": "",
        "waybar_timezone": "",
        "waybar_workspaces": 5,
        "rofi_bordersize": 3,
        "waybar_appmenu": True,
        "waybar_taskbar": False,
        "waybar_quicklinks": True,
        "waybar_network": True,
        "waybar_systray": True,
        "waybar_screenlock": True,
        "waybar_window": True,
        "waybar_settings": True
    }

    # {: time date}
    timeformats = [
        "%H:%M",
        "%I:%M",
        "%I:%M %p"
    ]

    dateformats = [
        "%a",
        "%A",
        "%a %Od",
        "%Od.%Om.%y",
        "%Od.%Om.%Y",
        "%a %Od.%Om.%y",
        "%a %Od.%Om.%Y",
        "%Om/%Od/%y",
        "%Om/%Od/%Y"
    ]

    timeformat = ""
    dateformat = ""

    waybar_show_appmenu = Gtk.Template.Child()
    waybar_show_taskbar = Gtk.Template.Child()
    waybar_show_quicklinks = Gtk.Template.Child()
    waybar_show_network = Gtk.Template.Child()
    waybar_show_systray = Gtk.Template.Child()
    waybar_show_screenlock = Gtk.Template.Child()
    waybar_show_window = Gtk.Template.Child()
    waybar_toggle = Gtk.Template.Child()
    wallpaper_cache_toggle = Gtk.Template.Child()
    gamemode_toggle = Gtk.Template.Child()
    dock_toggle = Gtk.Template.Child()
    rofi_font = Gtk.Template.Child()
    rofi_bordersize = Gtk.Template.Child()
    waybar_workspaces = Gtk.Template.Child()
    default_browser = Gtk.Template.Child()
    default_email = Gtk.Template.Child()
    default_filemanager = Gtk.Template.Child()
    default_editor = Gtk.Template.Child()
    default_networkmanager = Gtk.Template.Child()
    default_bluetooth = Gtk.Template.Child()
    default_softwaremanager = Gtk.Template.Child()
    default_terminal = Gtk.Template.Child()
    default_screenshoteditor = Gtk.Template.Child()
    default_calculator = Gtk.Template.Child()
    default_systemmonitor = Gtk.Template.Child()
    default_emojipicker = Gtk.Template.Child()
    default_aurhelper = Gtk.Template.Child()
    default_installupdates = Gtk.Template.Child()
    open_customconf = Gtk.Template.Child()
    open_quicklinks = Gtk.Template.Child()
    open_wallpaper_effects = Gtk.Template.Child()
    open_waybar_folder = Gtk.Template.Child()
    open_timeformatspecifications = Gtk.Template.Child()
    dd_wallpaper_effects = Gtk.Template.Child()
    dd_animations = Gtk.Template.Child()
    dd_environments = Gtk.Template.Child()
    dd_layouts = Gtk.Template.Child()
    dd_monitors = Gtk.Template.Child()
    dd_decorations = Gtk.Template.Child()
    dd_windows = Gtk.Template.Child()
    dd_workspaces = Gtk.Template.Child()
    dd_windowrules = Gtk.Template.Child()
    dd_keybindings = Gtk.Template.Child()
    dd_timeformats = Gtk.Template.Child()
    dd_dateformats = Gtk.Template.Child()
    custom_datetime = Gtk.Template.Child()
    custom_timezone = Gtk.Template.Child()
    blur_radius = Gtk.Template.Child()
    blur_sigma = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load Settings
        result = []
        for k, v in self.settings.items():
            v = self.loadSettingBash(k + ".sh")
            result.append({'key': k, 'value': v})

        for row in result:
            self.settings[row["key"]] = row["value"]

        self.loadDefaultApp("ml4w/settings/browser.sh",self.default_browser)
        self.loadDefaultApp("ml4w/settings/email.sh",self.default_email)
        self.loadDefaultApp("ml4w/settings/filemanager.sh",self.default_filemanager)
        self.loadDefaultApp("ml4w/settings/editor.sh",self.default_editor)
        self.loadDefaultApp("ml4w/settings/networkmanager.sh",self.default_networkmanager)
        self.loadDefaultApp("ml4w/settings/bluetooth.sh",self.default_bluetooth)
        self.loadDefaultApp("ml4w/settings/software.sh",self.default_softwaremanager)
        self.loadDefaultApp("ml4w/settings/terminal.sh",self.default_terminal)
        self.loadDefaultApp("ml4w/settings/screenshot-editor.sh",self.default_screenshoteditor)
        self.loadDefaultApp("ml4w/settings/calculator.sh",self.default_calculator)
        self.loadDefaultApp("ml4w/settings/system-monitor.sh",self.default_systemmonitor)
        self.loadDefaultApp("ml4w/settings/emojipicker.sh",self.default_emojipicker)
        self.loadDefaultApp("ml4w/settings/aur.sh",self.default_aurhelper)
        self.loadDefaultApp("ml4w/settings/installupdates.sh",self.default_installupdates)

        self.loadWallpaperEffects(self.dd_wallpaper_effects)
        self.loadVariations(self.dd_animations,"animation")
        self.loadVariations(self.dd_environments,"environment")
        self.loadVariations(self.dd_layouts,"layout")
        self.loadVariations(self.dd_monitors,"monitor")
        self.loadVariations(self.dd_decorations,"decoration")
        self.loadVariations(self.dd_windows,"window")
        self.loadVariations(self.dd_workspaces,"workspace")
        self.loadVariations(self.dd_windowrules,"windowrule")
        self.loadVariations(self.dd_keybindings,"keybinding")
        self.loadDropDown(self.dd_timeformats,self.timeformats,"waybar_timeformat")
        self.loadDropDown(self.dd_dateformats,self.dateformats,"waybar_dateformat")

        self.loadShowModule("waybar_taskbar",self.waybar_show_taskbar)
        self.loadShowModule("waybar_appmenu",self.waybar_show_appmenu)
        self.loadShowModule("waybar_quicklinks",self.waybar_show_quicklinks)
        self.loadShowModule("waybar_window",self.waybar_show_window)
        self.loadShowModule("waybar_network",self.waybar_show_network)
        self.loadShowModule("waybar_systray",self.waybar_show_systray)
        self.loadShowModule("waybar_screenlock",self.waybar_show_screenlock)

        self.loadGamemode()
        self.loadDock()
        self.loadWaybar()
        self.loadWallpaperCache()
        self.loadRofiFont()
        self.loadBlurValues()

        self.getTerminal()

        self.custom_datetime.set_show_apply_button(True)
        self.custom_datetime.set_text(self.settings["waybar_custom_timedateformat"])

        self.custom_timezone.set_show_apply_button(True)
        self.custom_timezone.set_text(self.settings["waybar_timezone"])

        # Settings
        self.waybar_workspaces.get_adjustment().set_value(int(self.settings["waybar_workspaces"]))
        self.rofi_bordersize.get_adjustment().set_value(int(self.settings["rofi_bordersize"]))

    # Load default app
    def loadDefaultApp(self,f,d):
        if os.path.exists(self.dotfiles + f):
            with open(self.dotfiles + f, 'r') as file:
                value = file.read()
            d.set_text(value.strip())
            d.set_show_apply_button(True)
        else:
            d.set_text("")
            d.set_editable(False)
            print("ERROR: File not found " + self.dotfiles + f)

    # Load setting from bash file
    def loadSettingBash(self,f):
        with open(self.dotfiles + "ml4w/settings/" + f, 'r') as file:
            value = file.read()
        return value.strip()

    # Load Wallpaper Effects from folder
    def loadWallpaperEffects(self,dd):
        files_arr = os.listdir(self.dotfiles + "hypr/effects/wallpaper/")
        store = Gtk.StringList()
        with open(self.dotfiles + "ml4w/settings/wallpaper-effect.sh", 'r') as file:
            value = file.read()
        selected = 0
        counter = 1
        store.append("off")
        for f in files_arr:
            store.append(f)
            if f in value:
                selected = counter
            counter+=1
        dd.set_model(store)
        dd.set_selected(selected)

    # Load variations
    def loadVariations(self,dd,v):
        files_arr = os.listdir(self.dotfiles + "hypr/conf/" + v + "s")
        store = Gtk.StringList()
        with open(self.dotfiles + "hypr/conf/" + v + ".conf", 'r') as file:
            value = file.read()
        selected = 0
        counter = 0
        for f in files_arr:
            store.append(f)
            if f in value:
                selected = counter
            counter+=1
        dd.set_model(store)
        dd.set_selected(selected)

    # Load dropdown
    def loadDropDown(self,dd,d,v):
        store = Gtk.StringList()
        selected = 0
        counter = 0
        value = self.settings[v]
        for f in d:
            store.append(f)
            if f == value:
                selected = counter
            counter+=1
        dd.set_model(store)
        dd.set_selected(selected)

    # Load Show Module
    def loadShowModule(self,f,d):
       if f in self.settings:
            if self.settings[f] == "True":
                d.set_active(True)
            else:
                d.set_active(False)

    # Load Gamemode
    def loadGamemode(self):
        if os.path.isfile(self.homeFolder + "/.config/ml4w/settings/gamemode-enabled"):
            self.gamemode_toggle.set_active(True)
        else:
            self.gamemode_toggle.set_active(False)

    def loadDock(self):
        if os.path.isfile(self.homeFolder + "/.config/ml4w/settings/dock-disabled"):
            self.dock_toggle.set_active(False)
        else:
            self.dock_toggle.set_active(True)

    def loadWaybar(self):
        if os.path.isfile(self.homeFolder + "/.config/ml4w/settings/waybar-disabled"):
            self.waybar_toggle.set_active(False)
        else:
            self.waybar_toggle.set_active(True)

    def loadWallpaperCache(self):
        if os.path.isfile(self.dotfiles + "ml4w/settings/wallpaper_cache"):
            self.wallpaper_cache_toggle.set_active(True)
        else:
            self.wallpaper_cache_toggle.set_active(False)

    # Load Blur Values
    def loadBlurValues(self):
        with open(self.dotfiles + "ml4w/settings/blur.sh", 'r') as file:
            value = file.read().strip()
        value = value.split("x")
        self.blur_radius.get_adjustment().set_value(int(value[0]))
        self.blur_sigma.get_adjustment().set_value(int(value[1]))

    # Load Rofi Font
    def loadRofiFont(self):
        with open(self.dotfiles + "ml4w/settings/rofi-font.rasi", 'r') as file:
            value = file.read().strip()
        value = value.split('"')
        self.rofi_font.set_text(value[1])
        self.rofi_font.set_show_apply_button(True)

    def getTerminal(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/terminal.sh"], capture_output=True, text=True)
            self.terminal = result.stdout.strip()
            # print (":: Using Terminal " + self.terminal)
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/terminal.sh")
