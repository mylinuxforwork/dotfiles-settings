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
    waybar_toggle = Gtk.Template.Child()
    rofi_font = Gtk.Template.Child()
    rofi_bordersize = Gtk.Template.Child()
    waybar_workspaces = Gtk.Template.Child()
    default_browser = Gtk.Template.Child()
    default_filemanager = Gtk.Template.Child()
    default_editor = Gtk.Template.Child()
    default_networkmanager = Gtk.Template.Child()
    default_softwaremanager = Gtk.Template.Child()
    default_terminal = Gtk.Template.Child()
    open_customconf = Gtk.Template.Child()
    open_timeformatspecifications = Gtk.Template.Child()
    open_hypridle = Gtk.Template.Child()
    dd_animations = Gtk.Template.Child()
    dd_environments = Gtk.Template.Child()
    dd_monitors = Gtk.Template.Child()
    dd_decorations = Gtk.Template.Child()
    dd_windows = Gtk.Template.Child()
    dd_windowrules = Gtk.Template.Child()
    dd_keybindings = Gtk.Template.Child()
    dd_timeformats = Gtk.Template.Child()
    dd_dateformats = Gtk.Template.Child()
    dd_wallpaper_engines = Gtk.Template.Child()
    custom_datetime = Gtk.Template.Child()
    hypridle_hyprlock = Gtk.Template.Child()
    hypridle_dpms = Gtk.Template.Child()
    hypridle_suspend = Gtk.Template.Child()
    blur_radius = Gtk.Template.Child()
    blur_sigma = Gtk.Template.Child()

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
    settings = {
        "waybar_timeformat": "%H:%M",
        "waybar_dateformat": "%a",
        "waybar_custom_timedateformat": "",
        "waybar_workspaces": 5,
        "rofi_bordersize": 3,
        "waybar_toggle": True,
        "waybar_network": True,
        "waybar_chatgpt": True,
        "waybar_systray": True,
        "waybar_screenlock": True,
        "waybar_window": True,
        "hypridle_hyprlock_timeout": 600,
        "hypridle_dpms_timeout": 680,
        "hypridle_suspend_timeout": 1800
    }

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
        self.create_action('waybar_toggle', self.on_waybar_toggle)
        self.create_action('rofi_bordersize', self.on_rofi_bordersize)
        self.create_action('waybar_workspaces', self.on_waybar_workspaces)
        self.create_action('blur_radius', self.on_blur_radius)
        self.create_action('blur_sigma', self.on_blur_sigma)
        self.create_action('open_about_variations', self.on_open_about_variations)

        self.create_action('on_open_animations_folder', self.on_open_animations)
        self.create_action('on_edit_animations', self.on_edit_animations)
        self.create_action('on_reload_animations', self.on_reload_animations)

        self.create_action('on_open_decorations_folder', self.on_open_decorations)
        self.create_action('on_edit_decorations', self.on_edit_decorations)
        self.create_action('on_reload_decorations', self.on_reload_decorations)

        self.create_action('on_open_windows_folder', self.on_open_windows)
        self.create_action('on_edit_windows', self.on_edit_windows)
        self.create_action('on_reload_windows', self.on_reload_windows)

        self.create_action('on_open_monitors_folder', self.on_open_monitors)
        self.create_action('on_edit_monitors', self.on_edit_monitors)
        self.create_action('on_reload_monitors', self.on_reload_monitors)

        self.create_action('on_open_keybindings_folder', self.on_open_keybindings)
        self.create_action('on_edit_keybindings', self.on_edit_keybindings)
        self.create_action('on_reload_keybindings', self.on_reload_keybindings)

        self.create_action('on_open_environments_folder', self.on_open_environments)
        self.create_action('on_edit_environments', self.on_edit_environments)
        self.create_action('on_reload_environments', self.on_reload_environments)

        self.create_action('on_open_windowrules_folder', self.on_open_windowrules)
        self.create_action('on_edit_windowrules', self.on_edit_windowrules)
        self.create_action('on_reload_windowrules', self.on_reload_windowrules)

    def do_activate(self):
        # Define main window
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        # Setup settings
        if not os.path.exists(self.dotfiles + ".settings/settings.json"):
            result = []
            for k, v in self.settings.items():
                result.append({'key': k, 'value': v})
            self.writeToSettings(result)

        # Load settings
        settings_file = open(self.dotfiles + ".settings/settings.json")
        settings_arr = json.load(settings_file)
        for row in settings_arr:
            self.settings[row["key"]] = row["value"]

        self.waybar_show_network = win.waybar_show_network
        self.waybar_show_chatgpt = win.waybar_show_chatgpt
        self.waybar_show_systray = win.waybar_show_systray
        self.waybar_show_screenlock = win.waybar_show_screenlock
        self.waybar_show_window = win.waybar_show_window
        self.waybar_toggle = win.waybar_toggle
        self.waybar_workspaces = win.waybar_workspaces
        self.hypridle_hyprlock = win.hypridle_hyprlock
        self.hypridle_dpms = win.hypridle_dpms
        self.hypridle_suspend = win.hypridle_suspend
        self.rofi_bordersize = win.rofi_bordersize
        self.rofi_font = win.rofi_font
        self.default_browser = win.default_browser
        self.default_filemanager = win.default_filemanager
        self.default_editor = win.default_editor
        self.default_networkmanager = win.default_networkmanager
        self.default_softwaremanager = win.default_softwaremanager
        self.default_terminal = win.default_terminal
        self.open_customconf = win.open_customconf
        self.open_timeformatspecifications = win.open_timeformatspecifications
        self.open_hypridle = win.open_hypridle
        self.dd_animations = win.dd_animations
        self.dd_environments = win.dd_environments
        self.dd_monitors = win.dd_monitors
        self.dd_decorations = win.dd_decorations
        self.dd_windows = win.dd_windows
        self.dd_windowrules = win.dd_windowrules
        self.dd_keybindings = win.dd_keybindings
        self.dd_timeformats = win.dd_timeformats
        self.dd_dateformats = win.dd_dateformats
        self.dd_wallpaper_engines = win.dd_wallpaper_engines
        self.custom_datetime = win.custom_datetime
        self.blur_radius = win.blur_radius
        self.blur_sigma = win.blur_sigma

        self.open_customconf.connect("clicked", self.on_open_customconf)
        self.open_timeformatspecifications.connect("clicked", self.on_open_timeformatspecifications)
        self.open_hypridle.connect("clicked", self.on_open_hypridle)

        self.waybar_workspaces.get_adjustment().connect("value-changed", self.on_waybar_workspaces)
        self.rofi_bordersize.get_adjustment().connect("value-changed", self.on_rofi_bordersize)
        self.blur_radius.get_adjustment().connect("value-changed", self.on_blur_radius)
        self.blur_sigma.get_adjustment().connect("value-changed", self.on_blur_sigma)

        self.rofi_font.connect("apply", self.on_rofi_font)
        self.hypridle_hyprlock.get_adjustment().connect("value-changed", self.on_hypridle_hyprlock)
        self.hypridle_dpms.get_adjustment().connect("value-changed", self.on_hypridle_dpms)
        self.hypridle_suspend.get_adjustment().connect("value-changed", self.on_hypridle_suspend)

        self.default_browser.connect("apply", self.on_default_browser)
        self.default_filemanager.connect("apply", self.on_default_filemanager)
        self.default_editor.connect("apply", self.on_default_editor)
        self.default_networkmanager.connect("apply", self.on_default_networkmanager)
        self.default_softwaremanager.connect("apply", self.on_default_softwaremanager)
        self.default_terminal.connect("apply", self.on_default_terminal)

        self.dd_animations.connect("notify::selected-item", self.on_variation_changed,"animation")
        self.dd_monitors.connect("notify::selected-item", self.on_variation_changed,"monitor")
        self.dd_environments.connect("notify::selected-item", self.on_variation_changed,"environment")
        self.dd_decorations.connect("notify::selected-item", self.on_variation_changed,"decoration")
        self.dd_windows.connect("notify::selected-item", self.on_variation_changed,"window")
        self.dd_windowrules.connect("notify::selected-item", self.on_variation_changed,"windowrule")
        self.dd_keybindings.connect("notify::selected-item", self.on_variation_changed,"keybinding")
        self.dd_wallpaper_engines.connect("notify::selected-item", self.on_wallpaper_engines_changed)

        self.dd_timeformats.connect("notify::selected-item", self.on_timeformats_changed)
        self.dd_dateformats.connect("notify::selected-item", self.on_dateformats_changed)

        self.loadVariations(self.dd_animations,"animation")
        self.loadVariations(self.dd_environments,"environment")
        self.loadVariations(self.dd_monitors,"monitor")
        self.loadVariations(self.dd_decorations,"decoration")
        self.loadVariations(self.dd_windows,"window")
        self.loadVariations(self.dd_windowrules,"windowrule")
        self.loadVariations(self.dd_keybindings,"keybinding")
        self.loadWallpaperEngine()


        self.loadDropDown(self.dd_timeformats,self.timeformats,"waybar_timeformat")
        self.loadDropDown(self.dd_dateformats,self.dateformats,"waybar_dateformat")
        self.custom_datetime.set_show_apply_button(True)
        self.custom_datetime.set_text(self.settings["waybar_custom_timedateformat"])
        self.custom_datetime.connect("apply", self.on_custom_datetime)

        self.loadShowModule("waybar_toggle",self.waybar_toggle)
        self.loadShowModule("waybar_window",self.waybar_show_window)
        self.loadShowModule("waybar_network",self.waybar_show_network)
        self.loadShowModule("waybar_chatgpt",self.waybar_show_chatgpt)
        self.loadShowModule("waybar_systray",self.waybar_show_systray)
        self.loadShowModule("waybar_screenlock",self.waybar_show_screenlock)

        self.waybar_workspaces.get_adjustment().set_value(self.settings["waybar_workspaces"])        
        self.rofi_bordersize.get_adjustment().set_value(self.settings["rofi_bordersize"])        

        self.loadDefaultApp(".settings/browser.sh",self.default_browser)
        self.loadDefaultApp(".settings/filemanager.sh",self.default_filemanager)
        self.loadDefaultApp(".settings/editor.sh",self.default_editor)
        self.loadDefaultApp(".settings/networkmanager.sh",self.default_networkmanager)
        self.loadDefaultApp(".settings/software.sh",self.default_softwaremanager)
        self.loadDefaultApp(".settings/terminal.sh",self.default_terminal)

        self.loadRofiFont()
        self.loadBlurValues()

        self.block_reload = False

        # Show Application Window
        win.present()
        print (":: Welcome to ML4W Dotfiles Settings App")

    def on_open_hypridle(self, widget):
        subprocess.Popen([self.default_editor.get_text(), self.dotfiles + "hypr/hypridle.conf"])

    def on_open_customconf(self, widget):
        subprocess.Popen([self.default_editor.get_text(), self.dotfiles + "hypr/conf/custom.conf"])

    def on_open_timeformatspecifications(self, widget):
        subprocess.Popen([self.default_browser.get_text(), "https://fmt.dev/latest/syntax.html#chrono-specs"])

    def on_open_about_variations(self, widget, _):
        subprocess.Popen([self.default_browser.get_text(), "https://gitlab.com/stephan-raabe/dotfiles/-/blob/main/hypr/conf/README.md"])

    def loadWallpaperEngine(self):
        with open(self.dotfiles + ".settings/wallpaper-engine.sh", 'r') as file:
            value = file.read()
        engine_arr = ["swww","hyprpaper","disabled"]
        store = Gtk.StringList()
        selected = 0
        counter = 0
        for f in engine_arr:
            store.append(f)
            if f in value:
                selected = counter
            counter+=1
        self.dd_wallpaper_engines.set_model(store)
        self.dd_wallpaper_engines.set_selected(selected)

    def on_wallpaper_engines_changed(self,widget,*data):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile(".settings/wallpaper-engine.sh", value)

    def loadShowModule(self,f,d):
       if f in self.settings:
            if self.settings[f]:
                d.set_active(True)
            else:
                d.set_active(False)

    def loadBlurValues(self):
        with open(self.dotfiles + ".settings/blur.sh", 'r') as file:
            value = file.read().strip()
        value = value.split("x")
        self.blur_radius.get_adjustment().set_value(int(value[0]))        
        self.blur_sigma.get_adjustment().set_value(int(value[1]))        

    def loadRofiFont(self):
        with open(self.dotfiles + ".settings/rofi-font.rasi", 'r') as file:
            value = file.read().strip()
        value = value.split('"')
        self.rofi_font.set_text(value[1])
        self.rofi_font.set_show_apply_button(True)

    def loadDefaultApp(self,f,d):
        with open(self.dotfiles + f, 'r') as file:
            value = file.read()
        d.set_text(value.strip())
        d.set_show_apply_button(True)

    def on_variation_changed(self,widget,*data):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("hypr/conf/" + data[1] + ".conf", "source = ~/dotfiles/hypr/conf/" + data[1] + "s/" + value)

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
            timedate = '        "format": "{:' + value + ' - ' + dateformat + '}",'
            self.updateSettings("waybar_timeformat", value)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.reloadWaybar()

    def on_dateformats_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '        "format": "{:' + timeformat + ' - ' + value + '}",'
            self.updateSettings("waybar_dateformat", value)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.reloadWaybar()

    def on_custom_datetime(self, widget):
        value = widget.get_text()
        if value != "":
            self.updateSettings("waybar_custom_timedateformat", value)
            timedate = '        "format": "{:' + value + '}",'
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"' '"format"', timedate)
        else:
            dateformat = self.dd_dateformats.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '        "format": "{:' + timeformat + ' - ' + dateformat + '}",'
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"' '"format"', timedate)
            self.updateSettings("waybar_custom_timedateformat", "")
        self.reloadWaybar()

    def on_open_animations(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/animations")

    def on_reload_animations(self, widget, _):
        self.loadVariations(self.dd_animations,"animation")

    def on_edit_animations(self, widget, _):
        i = self.dd_animations.get_selected()
        f = self.dd_animations.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/animations/" + f)

    def on_open_environments(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/environments")

    def on_reload_environments(self, widget, _):
        self.loadVariations(self.dd_environments,"environment")

    def on_edit_environments(self, widget, _):
        i = self.dd_environments.get_selected()
        f = self.dd_environments.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/environments/" + f)

    def on_open_monitors(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/monitors")

    def on_reload_monitors(self, widget, _):
        self.loadVariations(self.dd_monitors,"monitor")

    def on_edit_monitors(self, widget, _):
        i = self.dd_monitors.get_selected()
        f = self.dd_monitors.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/monitors/" + f)

    def on_open_decorations(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/decorations")

    def on_reload_decorations(self, widget, _):
        self.loadVariations(self.dd_decorations,"decoration")

    def on_edit_decorations(self, widget, _):
        i = self.dd_decorations.get_selected()
        f = self.dd_decorations.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/decorations/" + f)

    def on_open_windows(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/windows")

    def on_reload_windows(self, widget, _):
        self.loadVariations(self.dd_windows,"window")

    def on_edit_windows(self, widget, _):
        i = self.dd_windows.get_selected()
        f = self.dd_windows.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/windows/" + f)

    def on_open_windowrules(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/windowrules")

    def on_reload_windowrules(self, widget, _):
        self.loadVariations(self.dd_windowrules,"windowrule")

    def on_edit_windowrules(self, widget, _):
        i = self.dd_windowrules.get_selected()
        f = self.dd_windowrules.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/windowrules/" + f)

    def on_open_keybindings(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/keybindings")

    def on_reload_keybindings(self, widget, _):
        self.loadVariations(self.dd_keybindings,"keybinding")

    def on_edit_keybindings(self, widget, _):
        i = self.dd_keybindings.get_selected()
        f = self.dd_keybindings.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/keybindings/" + f)

    def on_open(self, widget, a, u):
        subprocess.Popen([a, self.dotfiles + u])

    def on_default_browser(self, widget):
        self.overwriteFile(".settings/browser.sh",widget.get_text())

    def on_default_filemanager(self, widget):
        self.overwriteFile(".settings/filemanager.sh",widget.get_text())

    def on_default_editor(self, widget):
        self.overwriteFile(".settings/editor.sh",widget.get_text())

    def on_default_networkmanager(self, widget):
        self.overwriteFile(".settings/networkmanager.sh",widget.get_text())

    def on_default_softwaremanager(self, widget):
        self.overwriteFile(".settings/software.sh",widget.get_text())

    def on_default_terminal(self, widget):
        self.overwriteFile(".settings/terminal.sh",widget.get_text())

    def on_rofi_font(self, widget):
        value = 'configuration { font: "' + widget.get_text() + '"; }'
        self.overwriteFile(".settings/rofi-font.rasi",value)

    def on_hypridle_hyprlock(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '    timeout = ' + str(value)
            self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK TIMEOUT", text)
            if int(widget.get_value()) == 0:
                self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK ONTIMEOUT", "    # on-timeout = hyprlock")
            else:
                self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK ONTIMEOUT", "    on-timeout = hyprlock")
            self.updateSettings("hypridle_hyprlock_timeout", value)

    def on_hypridle_dpms(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '    timeout = ' + str(value)
            self.replaceInFileNext("hypr/hypridle.conf", "DPMS TIMEOUT", text)
            if int(widget.get_value()) == 0:
                self.replaceInFileNext("hypr/hypridle.conf", "DPMS ONTIMEOUT", "    # on-timeout = hyprctl dispatch dpms off")
                self.replaceInFileNext("hypr/hypridle.conf", "DPMS ONRESUME", "    # on-resume = hyprctl dispatch dpms on")
            else:
                self.replaceInFileNext("hypr/hypridle.conf", "DPMS ONTIMEOUT", "    on-timeout = hyprctl dispatch dpms off")
                self.replaceInFileNext("hypr/hypridle.conf", "DPMS ONRESUME", "    on-resume = hyprctl dispatch dpms on")
            self.updateSettings("hypridle_dpms_timeout", value)

    def on_hypridle_suspend(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '    timeout = ' + str(value)
            self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND TIMEOUT", text)
            if int(widget.get_value()) == 0:
                self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND ONTIMEOUT", "    # on-timeout = systemctl suspend")
            else:
                self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND ONTIMEOUT", "    on-timeout = systemctl suspend")
            self.updateSettings("hypridle_suspend_timeout", value)

    def on_waybar_workspaces(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '            "*": ' + str(value)
            self.replaceInFileCheckpoint("waybar/modules.json", "persistent-workspaces",'"*"', text)
            self.reloadWaybar()
            self.updateSettings("waybar_workspaces", value)

    def on_waybar_toggle(self, widget, _):
        if not self.block_reload:
            if (os.path.exists(self.homeFolder + "/.cache/waybar-disabled")):
                os.remove(self.homeFolder + "/.cache/waybar-disabled")
            else:
                file = open(self.homeFolder + "/.cache/waybar-disabled", "w+")
            self.reloadWaybar()

    def on_rofi_bordersize(self, widget):
        value = int(widget.get_value())
        text = "* { border-width: " + str(value) + "px; }"
        self.overwriteFile(".settings/rofi-border.rasi",text)
        self.updateSettings("rofi_bordersize", value)

    def on_blur_radius(self, widget):
        if not self.block_reload:
            radius = str(int(widget.get_value()))
            sigma = str(int(self.blur_sigma.get_adjustment().get_value()))
            text = radius + "x" + sigma
            self.overwriteFile(".settings/blur.sh",text)

    def on_blur_sigma(self, widget):
        if not self.block_reload:
            sigma = str(int(widget.get_value()))
            radius = str(int(self.blur_radius.get_adjustment().get_value()))
            text = radius + "x" + sigma
            self.overwriteFile(".settings/blur.sh",text)

    def on_waybar_show_network(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_network.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        "network",')
                self.updateSettings("waybar_network", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        //"network",')
                self.updateSettings("waybar_network", False)
            self.reloadWaybar()

    def on_waybar_show_window(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_window.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        "hyprland/window",')
                self.updateSettings("waybar_window", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        //"hyprland/window",')
                self.updateSettings("waybar_window", False)
            self.reloadWaybar()

    def on_waybar_show_systray(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_systray.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        "tray",')
                self.updateSettings("waybar_systray", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        //"tray",')
                self.updateSettings("waybar_systray", False)
            self.reloadWaybar()

    def on_waybar_show_screenlock(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_screenlock.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"idle_inhibitor"','        "idle_inhibitor",')
                self.updateSettings("waybar_screenlock", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"idle_inhibitor"','        //"idle_inhibitor",')
                self.updateSettings("waybar_screenlock", False)
            self.reloadWaybar()

    def on_waybar_show_chatgpt(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_chatgpt.get_active():
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/settings', '"custom/chatgpt"', '            "custom/chatgpt",')
                self.updateSettings("waybar_chatgpt", True)
            else:
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/settings', '"custom/chatgpt"', '//            "custom/chatgpt",')
                self.updateSettings("waybar_chatgpt", False)
            self.reloadWaybar()


    def updateSettings(self,keyword,value):
        result = []
        self.settings[keyword] = value
        for k, v in self.settings.items():
            result.append({'key': k, 'value': v})
        self.writeToSettings(result)

    def writeToSettings(self,result):
        with open(self.dotfiles + '.settings/settings.json', 'w+', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def searchInFile(self, f, search):
        with open(self.dotfiles + f, 'r') as file:
            content = file.read()
            if search in content:
                return True
            else:
                return False

    def overwriteFile(self, f, text):
        file=open(self.dotfiles + f,"w+")
        file.write(text)
        file.close()

    def replaceInFile(self, f, search, replace):
        file = open(self.dotfiles + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        for l in lines:
            count += 1
            if search in l:
                found = count
                break
        if found > 0:
            lines[found - 1] = replace + "\n"
            with open(self.dotfiles + f, 'w') as file:
                file.writelines(lines)

    def replaceInFileNext(self, f, search, replace):
        file = open(self.dotfiles + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        for l in lines:
            count += 1
            if search in l:
                found = count
                break
        if found > 0:
            lines[found] = replace + "\n"
            with open(self.dotfiles + f, 'w') as file:
                file.writelines(lines)

    def replaceInFileCheckpoint(self, f, checkpoint, search, replace):
        file = open(self.dotfiles + f, 'r')
        lines = file.readlines()
        count = 0
        checkpoint_found = 0
        found = 0
        for l in lines:
            count += 1
            if checkpoint in l:
                checkpoint_found = count
                break
        print("Checkpoint: " + str(checkpoint_found))

        count = 0
        if checkpoint_found > 0:
            for l in lines:
                count += 1
                if count > checkpoint_found:
                    if search in l:
                        found = count
                        break
        print("Found: " + str(found))

        if found > 0:
            lines[found-1] = replace + "\n"
            with open(self.dotfiles + f, 'w') as file:
                file.writelines(lines)

    def reloadWaybar(self):
        launch_script = self.dotfiles + "waybar/launch.sh"
        subprocess.Popen(["setsid", launch_script, "1>/dev/null" ,"2>&1" "&"])

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

# Application Start
app = MyApp()
sm = app.get_style_manager()
sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
app.run(sys.argv)