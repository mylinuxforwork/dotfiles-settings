#  __  __ _    _  ___        __      _       _    __ _ _           
# |  \/  | |  | || \ \      / /   __| | ___ | |_ / _(_) | ___  ___ 
# | |\/| | |  | || |\ \ /\ / /   / _` |/ _ \| __| |_| | |/ _ \/ __|
# | |  | | |__|__   _\ V  V /   | (_| | (_) | |_|  _| | |  __/\__ \
# |_|  |_|_____| |_|  \_/\_/     \__,_|\___/ \__|_| |_|_|\___||___/
#                                                                 
                                                             
import sys
import gi
import subprocess
import os
import threading
import json
import pathlib
import shutil

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
from gi.repository import GLib
from gi.repository import GObject

# Get script path
pathname = os.path.dirname(sys.argv[0])

# -----------------------------------------
# Define UI template
# -----------------------------------------
@Gtk.Template(filename = pathname + '/src/settings.ui')

# -----------------------------------------
# Main Window
# -----------------------------------------
class MainWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'Ml4wSettingsWindow'
    waybar_show_network = Gtk.Template.Child()
    waybar_show_chatgpt = Gtk.Template.Child()
    waybar_show_systray = Gtk.Template.Child()
    waybar_show_screenlock = Gtk.Template.Child()
    waybar_show_window = Gtk.Template.Child()
    rofi_bordersize = Gtk.Template.Child()
    waybar_workspaces = Gtk.Template.Child()
    default_browser = Gtk.Template.Child()
    default_filemanager = Gtk.Template.Child()
    default_networkmanager = Gtk.Template.Child()
    default_softwaremanager = Gtk.Template.Child()
    default_terminal = Gtk.Template.Child()
    open_animations = Gtk.Template.Child()
    open_environments = Gtk.Template.Child()
    open_monitors = Gtk.Template.Child()
    dd_animations = Gtk.Template.Child()
    dd_environments = Gtk.Template.Child()
    dd_monitors = Gtk.Template.Child()
    dd_timeformats = Gtk.Template.Child()
    dd_dateformats = Gtk.Template.Child()
    custom_datetime = Gtk.Template.Child()

    # Get objects from template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -----------------------------------------
# Main App
# -----------------------------------------
class MyApp(Adw.Application):
    win = Adw.ApplicationWindow() # Application Window
    path_name = pathname # Path of Application
    homeFolder = os.path.expanduser('~') # Path to home folder
    dotfiles = homeFolder + "/dotfiles/"
    block_reload = True
    settings = {}

    waybar_themes = [
        "ml4w-minimal",
        "ml4w",
        "ml4w-blur",
        "ml4w-blur-bottom",
        "ml4w-bottom"
    ]

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

    def __init__(self, **kwargs):
        super().__init__(application_id='com.ml4w.dotfilessettings',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('waybar_show_network', self.on_waybar_show_network)
        self.create_action('waybar_show_screenlock', self.on_waybar_show_screenlock)
        self.create_action('waybar_show_chatgpt', self.on_waybar_show_chatgpt)
        self.create_action('waybar_show_systray', self.on_waybar_show_systray)
        self.create_action('waybar_show_window', self.on_waybar_show_window)
        self.create_action('rofi_bordersize', self.on_rofi_bordersize)
        self.create_action('waybar_workspaces', self.on_waybar_workspaces)

    def do_activate(self):
        # Define main window
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        # Load settings
        if not os.path.exists(self.dotfiles + ".settings/settings.json"):
            shutil.copy(self.path_name + '/settings.json', self.dotfiles + ".settings/")
        settings_file = open(self.dotfiles + ".settings/settings.json")
        settings_arr = json.load(settings_file)
        for row in settings_arr:
            self.settings[row["key"]] = row["value"]

        self.waybar_show_network = win.waybar_show_network
        self.waybar_show_chatgpt = win.waybar_show_chatgpt
        self.waybar_show_systray = win.waybar_show_systray
        self.waybar_show_screenlock = win.waybar_show_screenlock
        self.waybar_show_window = win.waybar_show_window
        self.waybar_workspaces = win.waybar_workspaces
        self.rofi_bordersize = win.rofi_bordersize
        self.default_browser = win.default_browser
        self.default_filemanager = win.default_filemanager
        self.default_networkmanager = win.default_networkmanager
        self.default_softwaremanager = win.default_softwaremanager
        self.default_terminal = win.default_terminal
        self.open_animations = win.open_animations
        self.open_environments = win.open_environments
        self.open_monitors = win.open_monitors
        self.dd_animations = win.dd_animations
        self.dd_environments = win.dd_environments
        self.dd_monitors = win.dd_monitors
        self.dd_timeformats = win.dd_timeformats
        self.dd_dateformats = win.dd_dateformats
        self.custom_datetime = win.custom_datetime

        self.waybar_workspaces.get_adjustment().connect("value-changed", self.on_waybar_workspaces)
        self.rofi_bordersize.get_adjustment().connect("value-changed", self.on_rofi_bordersize)

        self.default_browser.connect("apply", self.on_default_browser)
        self.default_filemanager.connect("apply", self.on_default_filemanager)
        self.default_networkmanager.connect("apply", self.on_default_networkmanager)
        self.default_softwaremanager.connect("apply", self.on_default_softwaremanager)
        self.default_terminal.connect("apply", self.on_default_terminal)

        self.open_animations.connect("clicked", self.on_open_animations)
        self.open_environments.connect("clicked", self.on_open_environments)
        self.open_monitors.connect("clicked", self.on_open_monitors)

        self.dd_animations.connect("notify::selected-item", self.on_animation_changed)
        self.dd_monitors.connect("notify::selected-item", self.on_monitor_changed)
        self.dd_environments.connect("notify::selected-item", self.on_environment_changed)

        self.dd_timeformats.connect("notify::selected-item", self.on_timeformats_changed)
        self.dd_dateformats.connect("notify::selected-item", self.on_dateformats_changed)

        self.loadVariations(self.dd_animations,"animation")
        self.loadVariations(self.dd_environments,"environment")
        self.loadVariations(self.dd_monitors,"monitor")

        self.loadDropDown(self.dd_timeformats,self.timeformats,"waybar_timeformat")
        self.loadDropDown(self.dd_dateformats,self.dateformats,"waybar_dateformat")
        self.custom_datetime.set_show_apply_button(True)
        self.custom_datetime.set_text(self.settings["waybar_custom_timedateformat"])

        self.custom_datetime.connect("apply", self.on_custom_datetime)

        # Waybar Window
        if "waybar_window" in self.settings:
            if self.settings["waybar_window"]:
                self.waybar_show_window.set_active(True)
            else:
                self.waybar_show_window.set_active(False)

        # Waybar Network
        if "waybar_network" in self.settings:
            if self.settings["waybar_network"]:
                self.waybar_show_network.set_active(True)
            else:
                self.waybar_show_network.set_active(False)

        # Waybar ChatGPT
        if "waybar_chatgpt" in self.settings:
            if self.settings["waybar_chatgpt"]:
                self.waybar_show_chatgpt.set_active(True)
            else:
                self.waybar_show_chatgpt.set_active(False)

        # Waybar Systray
        if "waybar_systray" in self.settings:
            if self.settings["waybar_systray"]:
                self.waybar_show_systray.set_active(True)
            else:
                self.waybar_show_systray.set_active(False)

        # Waybar Screenlock
        if "waybar_screenlock" in self.settings:
            if self.settings["waybar_screenlock"]:
                self.waybar_show_screenlock.set_active(True)
            else:
                self.waybar_show_screenlock.set_active(False)

        # Waybar Workspaces
        if "waybar_workspaces" in self.settings:
            self.waybar_workspaces.get_adjustment().set_value(self.settings["waybar_workspaces"])        

        # Rofi Bordersize
        if "rofi_bordersize" in self.settings:
            self.rofi_bordersize.get_adjustment().set_value(self.settings["rofi_bordersize"])        

        # Default Browser
        with open(self.dotfiles + ".settings/browser.sh", 'r') as file:
            value = file.read()
        self.default_browser.set_text(value.strip())
        self.default_browser.set_show_apply_button(True)

        # Default Filemanager
        with open(self.dotfiles + ".settings/filemanager.sh", 'r') as file:
            value = file.read()
        self.default_filemanager.set_text(value.strip())
        self.default_filemanager.set_show_apply_button(True)

        # Default Networkmanager
        with open(self.dotfiles + ".settings/networkmanager.sh", 'r') as file:
            value = file.read()
        self.default_networkmanager.set_text(value.strip())
        self.default_networkmanager.set_show_apply_button(True)

        # Default Softwaremanager
        with open(self.dotfiles + ".settings/software.sh", 'r') as file:
            value = file.read()
        self.default_softwaremanager.set_text(value.strip())
        self.default_softwaremanager.set_show_apply_button(True)

        # Default Terminal
        with open(self.dotfiles + ".settings/terminal.sh", 'r') as file:
            value = file.read()
        self.default_terminal.set_text(value.strip())
        self.default_terminal.set_show_apply_button(True)

        self.block_reload = False

        # Show Application Window
        win.present()
        print (":: Welcome to ML4W Dotfiles Settings App")

    def on_animation_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("hypr/conf/animation.conf", "source = ~/dotfiles/hypr/conf/animations/" + value)

    def on_monitor_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("hypr/conf/monitor.conf", "source = ~/dotfiles/hypr/conf/monitors/" + value)

    def on_environment_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("hypr/conf/environment.conf", "source = ~/dotfiles/hypr/conf/environment/" + value)

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


    def on_timeformats_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            dateformat = self.dd_dateformats.get_selected_item().get_string()
            timedate = '"format": "{:' + value + ' - ' + dateformat + '}",'
            self.updateSettings("waybar_timeformat", value)
            self.replaceInFileNext("waybar/modules.json", "TIMEDATEFORMAT", timedate)
            self.reloadWaybar()

    def on_dateformats_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '"format": "{:' + timeformat + ' - ' + value + '}",'
            self.updateSettings("waybar_dateformat", value)
            self.replaceInFileNext("waybar/modules.json", "TIMEDATEFORMAT", timedate)
            self.reloadWaybar()

    def on_custom_datetime(self, widget):
        value = widget.get_text()
        if value != "":
            self.updateSettings("waybar_custom_timedateformat", value)
            timedate = '"format": "{:' + value + '}",'
            self.replaceInFileNext("waybar/modules.json", "TIMEDATEFORMAT", timedate)
        else:
            dateformat = self.dd_dateformats.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '"format": "{:' + timeformat + ' - ' + dateformat + '}",'
            self.replaceInFileNext("waybar/modules.json", "TIMEDATEFORMAT", timedate)
            self.updateSettings("waybar_custom_timedateformat", "")
        self.reloadWaybar()

    def on_open_animations(self,widget):
        subprocess.Popen(["xdg-open", self.dotfiles + "hypr/conf/animations"])

    def on_open_environments(self,widget):
        subprocess.Popen(["xdg-open", self.dotfiles + "hypr/conf/environments"])

    def on_open_monitors(self,widget):
        subprocess.Popen(["xdg-open", self.dotfiles + "hypr/conf/monitors"])

    def on_default_browser(self, widget):
        self.overwriteFile(".settings/browser.sh",widget.get_text())

    def on_default_filemanager(self, widget):
        self.overwriteFile(".settings/filemanager.sh",widget.get_text())

    def on_default_networkmanager(self, widget):
        self.overwriteFile(".settings/networkmanager.sh",widget.get_text())

    def on_default_softwaremanager(self, widget):
        self.overwriteFile(".settings/software.sh",widget.get_text())

    def on_default_terminal(self, widget):
        self.overwriteFile(".settings/terminal.sh",widget.get_text())

    def on_waybar_workspaces(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '"*": ' + str(value) + '\n'
            self.replaceInFileNext("waybar/modules.json", "// START WORKSPACES", text)
            self.reloadWaybar()
            self.updateSettings("waybar_workspaces", value)

    def on_rofi_bordersize(self, widget):
        value = int(widget.get_value())
        text = "* { border-width: " + str(value) + "px; }"
        self.overwriteFile(".settings/rofi-border.rasi",text)
        self.updateSettings("rofi_bordersize", value)

    def on_waybar_show_network(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_network.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','"network",')
                self.updateSettings("waybar_network", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','//"network",')
                self.updateSettings("waybar_network", False)
            self.reloadWaybar()

    def on_waybar_show_window(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_window.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','"hyprland/window",')
                self.updateSettings("waybar_window", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','//"hyprland/window",')
                self.updateSettings("waybar_window", False)
            self.reloadWaybar()

    def on_waybar_show_systray(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_systray.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','"tray",')
                self.updateSettings("waybar_systray", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','//"tray",')
                self.updateSettings("waybar_systray", False)
            self.reloadWaybar()


    def on_waybar_show_screenlock(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_screenlock.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"idle_inhibitor"','"idle_inhibitor",')
                self.updateSettings("waybar_screenlock", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"idle_inhibitor"','//"idle_inhibitor",')
                self.updateSettings("waybar_screenlock", False)
            self.reloadWaybar()

    def on_waybar_show_chatgpt(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_chatgpt.get_active():
                self.replaceInFile("waybar/modules.json",'"custom/chatgpt"','"custom/chatgpt",')
                self.updateSettings("waybar_chatgpt", True)
            else:
                self.replaceInFile("waybar/modules.json",'"custom/chatgpt"','//"custom/chatgpt",')
                self.updateSettings("waybar_chatgpt", False)
            self.reloadWaybar()

    def updateSettings(self,keyword,value):
        result = []
        self.settings[keyword] = value
        for k, v in self.settings.items():
            result.append({'key': k, 'value': v})
        self.writeToSettings(result)

    def writeToSettings(self,result):
        with open(self.dotfiles + '.settings/settings.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def searchInFile(self, f, search):
        with open(self.dotfiles + f, 'r') as file:
            content = file.read()
            if search in content:
                return True
            else:
                return False

    # Overwrite Text in File
    def overwriteFile(self, f, text):
        file=open(self.dotfiles + f,"w+")
        file.write(text)
        file.close()

    # Replace Text in File
    def replaceInFile(self, f, search, replace):
        print(f)
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
            print (found - 1)
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

    # Reload Waybar
    def reloadWaybar(self):
        launch_script = self.dotfiles + "waybar/launch.sh"
        subprocess.Popen(["setsid", launch_script, "1>/dev/null" ,"2>&1" "&"])

    # Add Application actions
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def changeTheme(self,win):
        app = win.get_application()
        sm = app.get_style_manager()
        sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

# Application Start
app = MyApp()
sm = app.get_style_manager()
sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
app.run(sys.argv)