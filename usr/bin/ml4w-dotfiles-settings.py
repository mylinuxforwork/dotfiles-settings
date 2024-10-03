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
import shlex

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

    # Get objects from template
    __gtype_name__ = 'Ml4wSettingsWindow'
    waybar_show_appmenu = Gtk.Template.Child()
    waybar_show_taskbar = Gtk.Template.Child()
    waybar_show_quicklinks = Gtk.Template.Child()
    waybar_show_network = Gtk.Template.Child()
    waybar_show_backlight = Gtk.Template.Child()
    waybar_show_chatgpt = Gtk.Template.Child()
    waybar_show_systray = Gtk.Template.Child()
    waybar_show_screenlock = Gtk.Template.Child()
    waybar_show_window = Gtk.Template.Child()
    waybar_toggle = Gtk.Template.Child()
    wallpaper_cache_toggle = Gtk.Template.Child()
    gamemode_toggle = Gtk.Template.Child()
    rofi_font = Gtk.Template.Child()
    rofi_bordersize = Gtk.Template.Child()
    waybar_workspaces = Gtk.Template.Child()
    default_browser = Gtk.Template.Child()
    default_filemanager = Gtk.Template.Child()
    default_editor = Gtk.Template.Child()
    default_networkmanager = Gtk.Template.Child()
    default_softwaremanager = Gtk.Template.Child()
    default_terminal = Gtk.Template.Child()
    default_screenshoteditor = Gtk.Template.Child()
    default_calculator = Gtk.Template.Child()
    default_systemmonitor = Gtk.Template.Child()
    default_emojipicker = Gtk.Template.Child()
    default_aurhelper = Gtk.Template.Child()
    open_customconf = Gtk.Template.Child()
    open_wallpaper_effects = Gtk.Template.Child()
    open_timeformatspecifications = Gtk.Template.Child()
    restart_hypridle = Gtk.Template.Child()
    dd_wallpaper_effects = Gtk.Template.Child()
    dd_animations = Gtk.Template.Child()
    dd_environments = Gtk.Template.Child()
    dd_monitors = Gtk.Template.Child()
    dd_decorations = Gtk.Template.Child()
    dd_windows = Gtk.Template.Child()
    dd_windowrules = Gtk.Template.Child()
    dd_keybindings = Gtk.Template.Child()
    dd_timeformats = Gtk.Template.Child()
    dd_dateformats = Gtk.Template.Child()
    dd_dunstpositions = Gtk.Template.Child()
    custom_datetime = Gtk.Template.Child()
    clock_interval = Gtk.Template.Child()
    hypridle_hyprlock = Gtk.Template.Child()
    hypridle_dpms = Gtk.Template.Child()
    hypridle_suspend = Gtk.Template.Child()
    blur_radius = Gtk.Template.Child()
    blur_sigma = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -----------------------------------------
# Main App
# -----------------------------------------
class MyApp(Adw.Application):
    win = Adw.ApplicationWindow() # Application Window
    path_name = pathname # Path of Application
    homeFolder = os.path.expanduser('~') # Path to home folder
    dotfiles = homeFolder + "/.config/"
    block_reload = True

    settings = {
        "waybar_timeformat": "%H:%M",
        "waybar_dateformat": "%a",
        "dunst_position": "top-center",
        "waybar_custom_timedateformat": "",
        "waybar_clock_interval": 60,
        "waybar_workspaces": 5,
        "rofi_bordersize": 3,
        "waybar_toggle": True,
        "waybar_appmenu": True,
        "waybar_taskbar": False,
        "waybar_quicklinks": True,
        "waybar_backlight": False,
        "waybar_network": True,
        "waybar_chatgpt": True,
        "waybar_systray": True,
        "waybar_screenlock": True,
        "waybar_window": True,
        "hypridle_hyprlock_timeout": 600,
        "hypridle_dpms_timeout": 660,
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

    dunstpositions = [
        "top-center",
        "top-right",
        "top-left"
    ]

    timeformat = ""
    dateformat = ""
    dunstposition = ""

    def __init__(self, **kwargs):
        super().__init__(application_id='com.ml4w.dotfilessettings',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('waybar_show_network', self.on_waybar_show_network)
        self.create_action('waybar_show_backlight', self.on_waybar_show_backlight)
        self.create_action('waybar_show_screenlock', self.on_waybar_show_screenlock)
        self.create_action('waybar_show_chatgpt', self.on_waybar_show_chatgpt)
        self.create_action('waybar_show_systray', self.on_waybar_show_systray)
        self.create_action('waybar_show_window', self.on_waybar_show_window)
        self.create_action('waybar_show_appmenu', self.on_waybar_show_appmenu)
        self.create_action('waybar_show_taskbar', self.on_waybar_show_taskbar)
        self.create_action('waybar_show_quicklinks', self.on_waybar_show_quicklinks)
        self.create_action('waybar_toggle', self.on_waybar_toggle)
        self.create_action('wallpaper_cache_toggle', self.on_wallpaper_cache_toggle)
        self.create_action('gamemode_toggle', self.on_gamemode_toggle)
        self.create_action('rofi_bordersize', self.on_rofi_bordersize)
        self.create_action('waybar_workspaces', self.on_waybar_workspaces)
        self.create_action('blur_radius', self.on_blur_radius)
        self.create_action('blur_sigma', self.on_blur_sigma)
        self.create_action('open_about_variations', self.on_open_about_variations)
        self.create_action('on_edit_wallpaper_effects', self.on_edit_animations)
        self.create_action('on_clearcache_wallpaper', self.on_clearcache_wallpaper)
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

        # Load Settings
        result = []
        for k, v in self.settings.items():
            v = self.loadSettingBash(k + ".sh")
            result.append({'key': k, 'value': v})

        for row in result:
            self.settings[row["key"]] = row["value"]

        self.waybar_show_network = win.waybar_show_network
        self.waybar_show_backlight = win.waybar_show_backlight
        self.waybar_show_chatgpt = win.waybar_show_chatgpt
        self.waybar_show_systray = win.waybar_show_systray
        self.waybar_show_screenlock = win.waybar_show_screenlock
        self.waybar_show_window = win.waybar_show_window
        self.waybar_show_taskbar = win.waybar_show_taskbar
        self.waybar_show_appmenu = win.waybar_show_appmenu
        self.waybar_show_quicklinks = win.waybar_show_quicklinks
        self.waybar_toggle = win.waybar_toggle
        self.wallpaper_cache_toggle = win.wallpaper_cache_toggle
        self.waybar_workspaces = win.waybar_workspaces
        self.gamemode_toggle = win.gamemode_toggle
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
        self.default_screenshoteditor = win.default_screenshoteditor
        self.default_calculator = win.default_calculator
        self.default_systemmonitor = win.default_systemmonitor
        self.default_emojipicker = win.default_emojipicker
        self.default_aurhelper = win.default_aurhelper
        self.open_customconf = win.open_customconf
        self.open_wallpaper_effects = win.open_wallpaper_effects
        self.open_timeformatspecifications = win.open_timeformatspecifications
        self.restart_hypridle = win.restart_hypridle
        self.dd_wallpaper_effects = win.dd_wallpaper_effects
        self.dd_animations = win.dd_animations
        self.dd_environments = win.dd_environments
        self.dd_monitors = win.dd_monitors
        self.dd_decorations = win.dd_decorations
        self.dd_windows = win.dd_windows
        self.dd_windowrules = win.dd_windowrules
        self.dd_keybindings = win.dd_keybindings
        self.dd_timeformats = win.dd_timeformats
        self.dd_dateformats = win.dd_dateformats
        self.dd_dunstpositions = win.dd_dunstpositions
        self.custom_datetime = win.custom_datetime
        self.clock_interval = win.clock_interval
        self.blur_radius = win.blur_radius
        self.blur_sigma = win.blur_sigma

        self.open_customconf.connect("clicked", self.on_open_customconf)
        self.open_timeformatspecifications.connect("clicked", self.on_open_timeformatspecifications)
        self.restart_hypridle.connect("clicked", self.on_restart_hypridle)
        self.default_browser.connect("apply", self.on_default_browser)
        self.default_filemanager.connect("apply", self.on_default_filemanager)
        self.default_editor.connect("apply", self.on_default_editor)
        self.default_networkmanager.connect("apply", self.on_default_networkmanager)
        self.default_softwaremanager.connect("apply", self.on_default_softwaremanager)
        self.default_terminal.connect("apply", self.on_default_terminal)
        self.default_screenshoteditor.connect("apply", self.on_default_screenshoteditor)
        self.default_calculator.connect("apply", self.on_default_calculator)
        self.default_systemmonitor.connect("apply", self.on_default_systemmonitor)
        self.default_emojipicker.connect("apply", self.on_default_emojipicker)
        self.default_aurhelper.connect("apply", self.on_default_aurhelper)
        self.open_wallpaper_effects.connect("clicked", self.on_open_wallpaper_effects_folder)
        self.dd_wallpaper_effects.connect("notify::selected-item", self.on_wallpaper_effects_changed)
        self.dd_animations.connect("notify::selected-item", self.on_variation_changed,"animation")
        self.dd_monitors.connect("notify::selected-item", self.on_variation_changed,"monitor")
        self.dd_environments.connect("notify::selected-item", self.on_variation_changed,"environment")
        self.dd_decorations.connect("notify::selected-item", self.on_variation_changed,"decoration")
        self.dd_windows.connect("notify::selected-item", self.on_variation_changed,"window")
        self.dd_windowrules.connect("notify::selected-item", self.on_variation_changed,"windowrule")
        self.dd_keybindings.connect("notify::selected-item", self.on_variation_changed,"keybinding")
        self.dd_timeformats.connect("notify::selected-item", self.on_timeformats_changed)
        self.dd_dateformats.connect("notify::selected-item", self.on_dateformats_changed)
        self.dd_dunstpositions.connect("notify::selected-item", self.on_dunstpositions_changed)
        self.custom_datetime.connect("apply", self.on_custom_datetime)
        self.clock_interval.get_adjustment().connect("value-changed", self.on_clock_interval)
        self.clock_interval.get_adjustment().set_value(int(self.settings["waybar_clock_interval"]))

        self.waybar_workspaces.get_adjustment().connect("value-changed", self.on_waybar_workspaces)
        self.rofi_bordersize.get_adjustment().connect("value-changed", self.on_rofi_bordersize)
        self.blur_radius.get_adjustment().connect("value-changed", self.on_blur_radius)
        self.blur_sigma.get_adjustment().connect("value-changed", self.on_blur_sigma)
        self.rofi_font.connect("apply", self.on_rofi_font)
        self.hypridle_hyprlock.get_adjustment().connect("value-changed", self.on_hypridle_hyprlock)
        self.hypridle_dpms.get_adjustment().connect("value-changed", self.on_hypridle_dpms)
        self.hypridle_suspend.get_adjustment().connect("value-changed", self.on_hypridle_suspend)
        self.waybar_workspaces.get_adjustment().set_value(int(self.settings["waybar_workspaces"]))        
        self.rofi_bordersize.get_adjustment().set_value(int(self.settings["rofi_bordersize"]))
        self.hypridle_hyprlock.get_adjustment().set_value(int(self.settings["hypridle_hyprlock_timeout"]))   
        self.hypridle_dpms.get_adjustment().set_value(int(self.settings["hypridle_dpms_timeout"]))   
        self.hypridle_suspend.get_adjustment().set_value(int(self.settings["hypridle_suspend_timeout"]))   

        self.loadWallpaperEffects(self.dd_wallpaper_effects)
        self.loadVariations(self.dd_animations,"animation")
        self.loadVariations(self.dd_environments,"environment")
        self.loadVariations(self.dd_monitors,"monitor")
        self.loadVariations(self.dd_decorations,"decoration")
        self.loadVariations(self.dd_windows,"window")
        self.loadVariations(self.dd_windowrules,"windowrule")
        self.loadVariations(self.dd_keybindings,"keybinding")
        self.loadDropDown(self.dd_timeformats,self.timeformats,"waybar_timeformat")
        self.loadDropDown(self.dd_dateformats,self.dateformats,"waybar_dateformat")
        self.loadDropDown(self.dd_dunstpositions,self.dunstpositions,"dunst_position")
        self.loadShowModule("waybar_toggle",self.waybar_toggle)
        self.loadShowModule("waybar_taskbar",self.waybar_show_taskbar)
        self.loadShowModule("waybar_appmenu",self.waybar_show_appmenu)
        self.loadShowModule("waybar_quicklinks",self.waybar_show_quicklinks)
        self.loadShowModule("waybar_window",self.waybar_show_window)
        self.loadShowModule("waybar_network",self.waybar_show_network)
        self.loadShowModule("waybar_backlight",self.waybar_show_backlight)
        self.loadShowModule("waybar_chatgpt",self.waybar_show_chatgpt)
        self.loadShowModule("waybar_systray",self.waybar_show_systray)
        self.loadShowModule("waybar_screenlock",self.waybar_show_screenlock)
        self.loadDefaultApp("ml4w/settings/browser.sh",self.default_browser)
        self.loadDefaultApp("ml4w/settings/filemanager.sh",self.default_filemanager)
        self.loadDefaultApp("ml4w/settings/editor.sh",self.default_editor)
        self.loadDefaultApp("ml4w/settings/networkmanager.sh",self.default_networkmanager)
        self.loadDefaultApp("ml4w/settings/software.sh",self.default_softwaremanager)
        self.loadDefaultApp("ml4w/settings/terminal.sh",self.default_terminal)
        self.loadDefaultApp("ml4w/settings/screenshot-editor.sh",self.default_screenshoteditor)
        self.loadDefaultApp("ml4w/settings/calculator.sh",self.default_calculator)
        self.loadDefaultApp("ml4w/settings/system-monitor.sh",self.default_systemmonitor)
        self.loadDefaultApp("ml4w/settings/emojipicker.sh",self.default_emojipicker)
        self.loadDefaultApp("ml4w/settings/aur.sh",self.default_aurhelper)

        self.loadGamemode()
        self.loadWallpaperCache()
        self.loadRofiFont()
        self.loadBlurValues()

        self.custom_datetime.set_show_apply_button(True)
        self.custom_datetime.set_text(self.settings["waybar_custom_timedateformat"])

        self.block_reload = False

        # Show Application Window
        win.present()
        print (":: Welcome to ML4W Dotfiles Settings App")

    def on_restart_hypridle(self, widget):
        subprocess.Popen(["bash", self.dotfiles + "hypr/scripts/restart-hypridle.sh"])

    def on_open_customconf(self, widget):
        subprocess.Popen([self.default_editor.get_text(), self.dotfiles + "hypr/conf/custom.conf"])

    def on_open_timeformatspecifications(self, widget):
        subprocess.Popen([self.default_browser.get_text(), "https://fmt.dev/latest/syntax/#chrono-format-specifications"])

    def on_open_about_variations(self, widget, _):
        subprocess.Popen([self.default_browser.get_text(), "https://gitlab.com/stephan-raabe/dotfiles/-/blob/main/hypr/conf/README.md"])

    def loadGamemode(self):
        if os.path.isfile(self.homeFolder + "/.cache/gamemode"):
            self.gamemode_toggle.set_active(True)
        else:
            self.gamemode_toggle.set_active(False)

    def loadWallpaperCache(self):
        if os.path.isfile(self.dotfiles + "ml4w/settings/wallpaper_cache"):
            self.wallpaper_cache_toggle.set_active(True)
        else:
            self.wallpaper_cache_toggle.set_active(False)

    # Load Show Module
    def loadShowModule(self,f,d):
       if f in self.settings:
            if self.settings[f] == "True":
                d.set_active(True)
            else:
                d.set_active(False)

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

    # Load setting from bash file
    def loadSettingBash(self,f):
        with open(self.dotfiles + "ml4w/settings/" + f, 'r') as file:
            value = file.read()
        return value.strip()

    # Load default app
    def loadDefaultApp(self,f,d):
        with open(self.dotfiles + f, 'r') as file:
            value = file.read()
        d.set_text(value.strip())
        d.set_show_apply_button(True)

    def on_variation_changed(self,widget,*data):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("hypr/conf/" + data[1] + ".conf", "source = ~/.config/hypr/conf/" + data[1] + "s/" + value)

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

    def on_clearcache_wallpaper(self, widget, _):
        subprocess.Popen(["bash", self.dotfiles + "hypr/scripts/wallpaper-cache.sh", "clearcache"])

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

    def on_dunstpositions_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            dunstposition = self.dd_dunstpositions.get_selected_item().get_string()
            dunstorigin = '    origin = ' + value
            self.updateSettingsBash("dunst_position", value)
            self.replaceInFile("dunst/dunstrc","origin =",dunstorigin)

    def on_timeformats_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            dateformat = self.dd_dateformats.get_selected_item().get_string()
            timedate = '        "format": "{:' + value + ' - ' + dateformat + '}",'
            self.updateSettingsBash("waybar_timeformat", value)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.replaceInFileCheckpoint("hypr/hyprlock.conf", 'clock', 'cmd[update:1000]', '    text = cmd[update:1000] echo "$(date +"' + value + '")"')
            self.reloadWaybar()

    def on_dateformats_changed(self,widget,_):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '        "format": "{:' + timeformat + ' - ' + value + '}",'
            self.updateSettingsBash("waybar_dateformat", value)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.reloadWaybar()

    def on_custom_datetime(self, widget):
        value = widget.get_text()
        if value != "":
            timedate = '        "format": "{:' + value + '}",'
            print(timedate)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.updateSettingsBash("waybar_custom_timedateformat", value)
        else:
            dateformat = self.dd_dateformats.get_selected_item().get_string()
            timeformat = self.dd_timeformats.get_selected_item().get_string()
            timedate = '        "format": "{:' + timeformat + ' - ' + dateformat + '}",'
            print(timedate)
            self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
            self.updateSettingsBash("waybar_custom_timedateformat", "")
        self.reloadWaybar()

    def on_clock_interval(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '        "interval": ' + str(value)
            self.replaceInFileCheckpoint("waybar/modules.json", "clock",'"interval"', text)
            self.reloadWaybar()
            self.updateSettingsBash("waybar_clock_interval", value)

    def on_wallpaper_effects_changed(self, widget, _):
        if not self.block_reload:
            value = widget.get_selected_item().get_string()
            self.overwriteFile("ml4w/settings/wallpaper-effect.sh", value)

    def on_open_wallpaper_effects_folder(self, widget):
        print("drin")
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/effects/wallpaper")

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
        a = shlex.split(a, posix=False)
        print(self.dotfiles + u)
        subprocess.Popen([*a, self.dotfiles + u])        

    def on_default_browser(self, widget):
        self.overwriteFile("ml4w/settings/browser.sh",widget.get_text())

    def on_default_filemanager(self, widget):
        self.overwriteFile("ml4w/settings/filemanager.sh",widget.get_text())

    def on_default_editor(self, widget):
        self.overwriteFile("ml4w/settings/editor.sh",widget.get_text())

    def on_default_networkmanager(self, widget):
        self.overwriteFile("ml4w/settings/networkmanager.sh",widget.get_text())

    def on_default_softwaremanager(self, widget):
        self.overwriteFile("ml4w/settings/software.sh",widget.get_text())

    def on_default_terminal(self, widget):
        self.overwriteFile("ml4w/settings/terminal.sh",widget.get_text())

    def on_default_screenshoteditor(self, widget):
        self.overwriteFile("ml4w/settings/screenshot-editor.sh",widget.get_text())

    def on_default_calculator(self, widget):
        self.overwriteFile("ml4w/settings/calculator.sh",widget.get_text())

    def on_default_systemmonitor(self, widget):
        self.overwriteFile("ml4w/settings/system-monitor.sh",widget.get_text())

    def on_default_emojipicker(self, widget):
        self.overwriteFile("ml4w/settings/emojipicker.sh",widget.get_text())

    def on_default_aurhelper(self, widget):
        self.overwriteFile("ml4w/settings/aur.sh",widget.get_text())

    def on_rofi_font(self, widget):
        value = 'configuration { font: "' + widget.get_text() + '"; }'
        self.overwriteFile("ml4w/settings/rofi-font.rasi",value)

    def on_hypridle_hyprlock(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '    timeout = ' + str(value)
            self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK TIMEOUT", text)
            if int(widget.get_value()) == 0:
                self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK ONTIMEOUT", "    # on-timeout = loginctl lock-session")
            else:
                self.replaceInFileNext("hypr/hypridle.conf", "HYPRLOCK ONTIMEOUT", "    on-timeout = loginctl lock-session")
            self.updateSettingsBash("hypridle_hyprlock_timeout", value)

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
            self.updateSettingsBash("hypridle_dpms_timeout", value)

    def on_hypridle_suspend(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '    timeout = ' + str(value)
            self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND TIMEOUT", text)
            if int(widget.get_value()) == 0:
                self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND ONTIMEOUT", "    # on-timeout = systemctl suspend")
            else:
                self.replaceInFileNext("hypr/hypridle.conf", "SUSPEND ONTIMEOUT", "    on-timeout = systemctl suspend")
            self.updateSettingsBash("hypridle_suspend_timeout", value)

    def on_waybar_workspaces(self, widget):
        if not self.block_reload:
            value = int(widget.get_value())
            text = '            "*": ' + str(value)
            self.replaceInFileCheckpoint("waybar/modules.json", "persistent-workspaces",'"*"', text)
            self.reloadWaybar()
            print(value)
            self.updateSettingsBash("waybar_workspaces", value)

    def on_gamemode_toggle(self, widget, _):
        if not self.block_reload:
            subprocess.Popen(["bash", self.dotfiles + "hypr/scripts/gamemode.sh"])

    def on_wallpaper_cache_toggle(self, widget, _):
        if not self.block_reload:
            if (os.path.exists(self.dotfiles + "ml4w/settings/wallpaper_cache")):
                os.remove(self.dotfiles + "ml4w/settings/wallpaper_cache")
            else:
                file = open(self.dotfiles + "ml4w/settings/wallpaper_cache", "w+")

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
        self.overwriteFile("ml4w/settings/rofi-border.rasi",text)
        self.updateSettingsBash("rofi_bordersize", value)

    def on_blur_radius(self, widget):
        if not self.block_reload:
            radius = str(int(widget.get_value()))
            sigma = str(int(self.blur_sigma.get_adjustment().get_value()))
            text = radius + "x" + sigma
            self.overwriteFile("ml4w/settings/blur.sh",text)

    def on_blur_sigma(self, widget):
        if not self.block_reload:
            sigma = str(int(widget.get_value()))
            radius = str(int(self.blur_radius.get_adjustment().get_value()))
            text = radius + "x" + sigma
            self.overwriteFile("ml4w/settings/blur.sh",text)

    def on_waybar_show_appmenu(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_appmenu.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"custom/appmenu"','        "custom/appmenu",')
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"custom/appmenuicon"','        "custom/appmenuicon",')
                self.updateSettingsBash("waybar_appmenu", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"custom/appmenu"','        //"custom/appmenu",')
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"custom/appmenuicon"','        //"custom/appmenuicon",')
                self.updateSettingsBash("waybar_appmenu", False)
            self.reloadWaybar()

    def on_waybar_show_taskbar(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_taskbar.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"wlr/taskbar"','        "wlr/taskbar",')
                self.updateSettingsBash("waybar_taskbar", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"wlr/taskbar"','        //"wlr/taskbar",')
                self.updateSettingsBash("waybar_taskbar", False)
            self.reloadWaybar()

    def on_waybar_show_quicklinks(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_quicklinks.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"group/quicklinks"','        "group/quicklinks",')
                self.updateSettingsBash("waybar_quicklinks", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"group/quicklinks"','        //"group/quicklinks",')
                self.updateSettingsBash("waybar_quicklinks", False)
            self.reloadWaybar()

    def on_waybar_show_network(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_network.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        "network",')
                self.updateSettingsBash("waybar_network", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        //"network",')
                self.updateSettingsBash("waybar_network", False)
            self.reloadWaybar()

    def on_waybar_show_backlight(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_backlight.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"backlight"','        "backlight",')
                self.updateSettingsBash("waybar_backlight", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"backlight"','        //"backlight",')
                self.updateSettingsBash("waybar_backlight", False)
            self.reloadWaybar()

    def on_waybar_show_window(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_window.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        "hyprland/window",')
                self.updateSettingsBash("waybar_window", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        //"hyprland/window",')
                self.updateSettingsBash("waybar_window", False)
            self.reloadWaybar()

    def on_waybar_show_systray(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_systray.get_active():
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        "tray",')
                self.updateSettingsBash("waybar_systray", True)
            else:
                for t in self.waybar_themes:
                    self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        //"tray",')
                self.updateSettingsBash("waybar_systray", False)
            self.reloadWaybar()

    def on_waybar_show_screenlock(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_screenlock.get_active():
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/tools', '"custom/hypridle"', '      "custom/hypridle",')
                self.updateSettingsBash("waybar_screenlock", True)
            else:
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/tools', '"custom/hypridle"', '//      "custom/hypridle",')
                self.updateSettingsBash("waybar_screenlock", False)
            self.reloadWaybar()

    def on_waybar_show_chatgpt(self, widget, _):
        if not self.block_reload:
            if self.waybar_show_chatgpt.get_active():
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/links', '"custom/chatgpt"', '      "custom/chatgpt",')
                self.updateSettingsBash("waybar_chatgpt", True)
            else:
                self.replaceInFileCheckpoint("waybar/modules.json", 'group/links', '"custom/chatgpt"', '//      "custom/chatgpt",')
                self.updateSettingsBash("waybar_chatgpt", False)
            self.reloadWaybar()


    def updateSettingsBash(self,keyword,value):
        self.overwriteFile("ml4w/settings/" + keyword + ".sh",value)

    def searchInFile(self, f, search):
        with open(self.dotfiles + f, 'r') as file:
            content = file.read()
            if search in content:
                return True
            else:
                return False

    def overwriteFile(self, f, text):
        file=open(self.dotfiles + f,"w+")
        file.write(str(text))
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