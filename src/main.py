# main.py
#
# Copyright 2025 Stephan Raabe
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

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import DotfilesSettingsWindow

# Get script path
pathname = os.path.dirname(sys.argv[0])

#The main application singleton class.
class DotfilesSettingsApplication(Adw.Application):

    path_name = pathname # Path of Application
    homeFolder = os.path.expanduser('~') # Path to home folder
    dotfiles = homeFolder + "/.config/"
    terminal = "alacritty"

    waybar_themes = [
        "ml4w-minimal",
        "ml4w",
        "ml4w-blur",
        "ml4w-blur-bottom",
        "ml4w-bottom",
        "ml4w-modern"
    ]

    def __init__(self):
        super().__init__(application_id='com.ml4w.settings',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
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
        self.create_action('on_open_workspaces_folder', self.on_open_workspaces)
        self.create_action('on_edit_workspaces', self.on_edit_workspaces)
        self.create_action('on_reload_workspaces', self.on_reload_workspaces)
        self.create_action('on_open_monitors_folder', self.on_open_monitors)
        self.create_action('on_edit_monitors', self.on_edit_monitors)
        self.create_action('on_reload_monitors', self.on_reload_monitors)
        self.create_action('on_open_keybindings_folder', self.on_open_keybindings)
        self.create_action('on_edit_keybindings', self.on_edit_keybindings)
        self.create_action('on_reload_keybindings', self.on_reload_keybindings)
        self.create_action('on_open_environments_folder', self.on_open_environments)
        self.create_action('on_edit_environments', self.on_edit_environments)
        self.create_action('on_reload_environments', self.on_reload_environments)
        self.create_action('on_open_layouts_folder', self.on_open_layouts)
        self.create_action('on_edit_layouts', self.on_edit_layouts)
        self.create_action('on_reload_layouts', self.on_reload_layouts)
        self.create_action('on_open_windowrules_folder', self.on_open_windowrules)
        self.create_action('on_edit_windowrules', self.on_edit_windowrules)
        self.create_action('on_reload_windowrules', self.on_reload_windowrules)

    # Called when the application is activated.
    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = DotfilesSettingsWindow(application=self)

        self.waybar_toggle = self.win.waybar_toggle
        self.wallpaper_cache_toggle = self.win.wallpaper_cache_toggle
        self.waybar_workspaces = self.win.waybar_workspaces
        self.rofi_bordersize = self.win.rofi_bordersize
        self.waybar_toggle = self.win.waybar_toggle
        self.rofi_font = self.win.rofi_font
        self.dock_toggle = self.win.dock_toggle
        self.gamemode_toggle = self.win.gamemode_toggle
        self.default_browser = self.win.default_browser
        self.default_email = self.win.default_email
        self.default_filemanager = self.win.default_filemanager
        self.default_editor = self.win.default_editor
        self.default_networkmanager = self.win.default_networkmanager
        self.default_softwaremanager = self.win.default_softwaremanager
        self.default_terminal = self.win.default_terminal
        self.default_screenshoteditor = self.win.default_screenshoteditor
        self.default_calculator = self.win.default_calculator
        self.default_systemmonitor = self.win.default_systemmonitor
        self.default_emojipicker = self.win.default_emojipicker
        self.default_aurhelper = self.win.default_aurhelper
        self.default_installupdates = self.win.default_installupdates
        self.dd_wallpaper_effects = self.win.dd_wallpaper_effects
        self.dd_animations = self.win.dd_animations
        self.dd_environments = self.win.dd_environments
        self.dd_layouts = self.win.dd_layouts
        self.dd_monitors = self.win.dd_monitors
        self.dd_decorations = self.win.dd_decorations
        self.dd_windows = self.win.dd_windows
        self.dd_workspaces = self.win.dd_workspaces
        self.dd_windowrules = self.win.dd_windowrules
        self.dd_keybindings = self.win.dd_keybindings
        self.dd_timeformats = self.win.dd_timeformats
        self.dd_dateformats = self.win.dd_dateformats
        self.custom_datetime = self.win.custom_datetime
        self.custom_timezone = self.win.custom_timezone
        self.blur_radius = self.win.blur_radius
        self.blur_sigma = self.win.blur_sigma

        self.win.waybar_toggle.connect("notify::active",self.on_waybar_toggle)
        self.win.waybar_show_appmenu.connect("notify::active",self.on_waybar_show_appmenu)
        self.win.waybar_show_taskbar.connect("notify::active",self.on_waybar_show_taskbar)
        self.win.waybar_show_quicklinks.connect("notify::active",self.on_waybar_show_quicklinks)
        self.win.waybar_show_network.connect("notify::active",self.on_waybar_show_network)
        self.win.waybar_show_screenlock.connect("notify::active",self.on_waybar_show_screenlock)
        self.win.waybar_show_chatgpt.connect("notify::active",self.on_waybar_show_chatgpt)
        self.win.waybar_show_systray.connect("notify::active",self.on_waybar_show_systray)
        self.win.waybar_show_window.connect("notify::active",self.on_waybar_show_window)
        self.win.dock_toggle.connect("notify::active",self.on_dock_toggle)
        self.win.gamemode_toggle.connect("notify::active",self.on_gamemode_toggle)
        self.win.wallpaper_cache_toggle.connect("notify::active",self.on_wallpaper_cache_toggle)

        self.win.open_customconf.connect("clicked", self.on_open_customconf)
        self.win.open_quicklinks.connect("clicked", self.on_open_quicklinks)
        self.win.open_wallpaper_effects.connect("clicked", self.on_open_wallpaper_effects_folder)
        self.win.open_waybar_folder.connect("clicked", self.on_open_waybar_folder)
        self.win.open_timeformatspecifications.connect("clicked", self.on_open_timeformatspecifications)

        self.win.default_browser.connect("apply", self.on_default_browser)
        self.win.default_email.connect("apply", self.on_default_email)
        self.win.default_filemanager.connect("apply", self.on_default_filemanager)
        self.win.default_editor.connect("apply", self.on_default_editor)
        self.win.default_networkmanager.connect("apply", self.on_default_networkmanager)
        self.win.default_softwaremanager.connect("apply", self.on_default_softwaremanager)
        self.win.default_terminal.connect("apply", self.on_default_terminal)
        self.win.default_screenshoteditor.connect("apply", self.on_default_screenshoteditor)
        self.win.default_calculator.connect("apply", self.on_default_calculator)
        self.win.default_systemmonitor.connect("apply", self.on_default_systemmonitor)
        self.win.default_emojipicker.connect("apply", self.on_default_emojipicker)
        self.win.default_aurhelper.connect("apply", self.on_default_aurhelper)
        self.win.default_installupdates.connect("apply", self.on_default_installupdates)

        self.dd_wallpaper_effects.connect("notify::selected-item", self.on_wallpaper_effects_changed)
        self.dd_animations.connect("notify::selected-item", self.on_variation_changed,"animation")
        self.dd_monitors.connect("notify::selected-item", self.on_variation_changed,"monitor")
        self.dd_environments.connect("notify::selected-item", self.on_variation_changed,"environment")
        self.dd_layouts.connect("notify::selected-item", self.on_variation_changed,"layout")
        self.dd_decorations.connect("notify::selected-item", self.on_variation_changed,"decoration")
        self.dd_windows.connect("notify::selected-item", self.on_variation_changed,"window")
        self.dd_workspaces.connect("notify::selected-item", self.on_variation_changed,"workspace")
        self.dd_windowrules.connect("notify::selected-item", self.on_variation_changed,"windowrule")
        self.dd_keybindings.connect("notify::selected-item", self.on_variation_changed,"keybinding")
        self.dd_timeformats.connect("notify::selected-item", self.on_timeformats_changed)
        self.dd_dateformats.connect("notify::selected-item", self.on_dateformats_changed)
        self.custom_datetime.connect("apply", self.on_custom_datetime)
        self.custom_timezone.connect("apply", self.on_custom_timezone)

        self.waybar_workspaces.get_adjustment().connect("value-changed", self.on_waybar_workspaces)
        self.rofi_bordersize.get_adjustment().connect("value-changed", self.on_rofi_bordersize)
        self.blur_radius.get_adjustment().connect("value-changed", self.on_blur_radius)
        self.blur_sigma.get_adjustment().connect("value-changed", self.on_blur_sigma)
        self.rofi_font.connect("apply", self.on_rofi_font)

        self.win.present()

    # Open editor with custom.conf
    def on_open_customconf(self, widget):
        subprocess.Popen(["flatpak-spawn", "--host", self.default_editor.get_text(), self.dotfiles + "hypr/conf/custom.conf"])

    # Open editor with quicklinks.conf
    def on_open_quicklinks(self, widget):
        subprocess.Popen(["flatpak-spawn", "--host", self.default_editor.get_text(), self.dotfiles + "ml4w/settings/waybar-quicklinks.json"])

    def on_open_timeformatspecifications(self, widget):
        subprocess.Popen(["flatpak-spawn", "--host", self.default_browser.get_text(), "https://fmt.dev/latest/syntax/#chrono-format-specifications"])

    def on_open_about_variations(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.default_browser.get_text(), "-new-window", "https://github.com/mylinuxforwork/dotfiles/wiki/Configuration-Variations"])

    # Load default app
    def loadDefaultApp(self,f,d):
        with open(self.dotfiles + f, 'r') as file:
            value = file.read()
        d.set_text(value.strip())
        d.set_show_apply_button(True)

    def on_variation_changed(self,widget,*data):
        value = widget.get_selected_item().get_string()
        self.overwriteFile("hypr/conf/" + data[1] + ".conf", "source = ~/.config/hypr/conf/" + data[1] + "s/" + value)

    def on_clearcache_wallpaper(self, widget, _):
        subprocess.Popen(["bash", self.dotfiles + "hypr/scripts/wallpaper-cache.sh"])

    def on_timeformats_changed(self,widget,_):
        value = widget.get_selected_item().get_string()
        dateformat = self.dd_dateformats.get_selected_item().get_string()
        timedate = '        "format": "{:' + value + ' - ' + dateformat + '}",'
        self.updateSettingsBash("waybar_timeformat", value)
        self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
        self.replaceInFileCheckpoint("hypr/hyprlock.conf", 'clock', 'cmd[update:1000]', '    text = cmd[update:1000] echo "$(date +"' + value + '")"')
        self.reloadWaybar()

    def on_dateformats_changed(self,widget,_):
        value = widget.get_selected_item().get_string()
        timeformat = self.dd_timeformats.get_selected_item().get_string()
        timedate = '        "format": "{:' + timeformat + ' - ' + value + '}",'
        self.updateSettingsBash("waybar_dateformat", value)
        self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"format"', timedate)
        self.reloadWaybar()

    def on_custom_timezone(self, widget):
        value = widget.get_text()
        timezone = '    "timezone": "' + value + '",'
        print(timezone)
        self.replaceInFileCheckpoint("waybar/modules.json", '"clock"', '"timezone"', timezone)
        self.updateSettingsBash("waybar_timezone", value)
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

    def on_wallpaper_effects_changed(self, widget, _):
        value = widget.get_selected_item().get_string()
        self.overwriteFile("ml4w/settings/wallpaper-effect.sh", value)
        subprocess.Popen(["flatpak-spawn", "--host", "bash", self.dotfiles + "hypr/scripts/wallpaper-effects.sh", "reload"])

    def on_open_wallpaper_effects_folder(self, widget):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/effects/wallpaper")

    def on_open_waybar_folder(self, widget):
        self.on_open(widget, self.default_filemanager.get_text(), "waybar")

    # --------------------------------------------------------------
    # VARIATIONS
    # --------------------------------------------------------------

    # Animation
    def on_open_animations(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/animations")

    def on_reload_animations(self, widget, _):
        self.win.loadVariations(self.dd_animations,"animation")

    def on_edit_animations(self, widget, _):
        i = self.dd_animations.get_selected()
        f = self.dd_animations.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/animations/" + f)

    # Environment
    def on_open_environments(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/environments")

    def on_reload_environments(self, widget, _):
        self.win.loadVariations(self.dd_environments,"environment")

    def on_edit_environments(self, widget, _):
        i = self.dd_environments.get_selected()
        f = self.dd_environments.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/environments/" + f)

    # Layouts
    def on_open_layouts(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/layouts")

    def on_reload_layouts(self, widget, _):
        self.win.loadVariations(self.dd_layouts,"layout")

    def on_edit_layouts(self, widget, _):
        i = self.dd_layouts.get_selected()
        f = self.dd_layouts.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/layouts/" + f)

    # Monitors
    def on_open_monitors(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/monitors")

    def on_reload_monitors(self, widget, _):
        self.win.loadVariations(self.dd_monitors,"monitor")

    def on_edit_monitors(self, widget, _):
        i = self.dd_monitors.get_selected()
        f = self.dd_monitors.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/monitors/" + f)

    # Decorations
    def on_open_decorations(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/decorations")

    def on_reload_decorations(self, widget, _):
        self.win.loadVariations(self.dd_decorations,"decoration")

    def on_edit_decorations(self, widget, _):
        i = self.dd_decorations.get_selected()
        f = self.dd_decorations.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/decorations/" + f)

    # Workspaces
    def on_open_workspaces(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/workspaces")

    def on_reload_workspaces(self, widget, _):
        self.win.loadVariations(self.dd_windows,"workspace")

    def on_edit_workspaces(self, widget, _):
        i = self.dd_workspaces.get_selected()
        f = self.dd_workspaces.get_model()[i].get_string()
        print(f)
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/workspaces/" + f)

    # Monitors
    def on_open_windows(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/windows")

    def on_reload_windows(self, widget, _):
        self.win.loadVariations(self.dd_windows,"window")

    def on_edit_windows(self, widget, _):
        i = self.dd_windows.get_selected()
        f = self.dd_windows.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/windows/" + f)

    # Window Rules
    def on_open_windowrules(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/windowrules")

    def on_reload_windowrules(self, widget, _):
        self.win.loadVariations(self.dd_windowrules,"windowrule")

    def on_edit_windowrules(self, widget, _):
        i = self.dd_windowrules.get_selected()
        f = self.dd_windowrules.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/windowrules/" + f)

    # Key Bindings
    def on_open_keybindings(self, widget, _):
        self.on_open(widget, self.default_filemanager.get_text(), "hypr/conf/keybindings")

    def on_reload_keybindings(self, widget, _):
        self.win.loadVariations(self.dd_keybindings,"keybinding")

    def on_edit_keybindings(self, widget, _):
        i = self.dd_keybindings.get_selected()
        f = self.dd_keybindings.get_model()[i].get_string()
        self.on_open(widget, self.default_editor.get_text(), "hypr/conf/keybindings/" + f)

    def on_open(self, widget, a, u):
        a = shlex.split(a, posix=False)
        subprocess.Popen(["flatpak-spawn", "--host", *a, self.dotfiles + u])

    # --------------------------------------------------------------
    # Default Apps
    # --------------------------------------------------------------

    def on_default_browser(self, widget):
        self.overwriteFile("ml4w/settings/browser.sh",widget.get_text())

    def on_default_email(self, widget):
        self.overwriteFile("ml4w/settings/email.sh",widget.get_text())

    def on_default_installupdates(self, widget):
        self.overwriteFile("ml4w/settings/installupdates.sh",widget.get_text())

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

    def on_waybar_workspaces(self, widget):
        value = int(widget.get_value())
        text = '            "*": ' + str(value)
        self.replaceInFileCheckpoint("waybar/modules.json", "persistent-workspaces",'"*"', text)
        self.reloadWaybar()
        print(value)
        self.updateSettingsBash("waybar_workspaces", value)

    def on_gamemode_toggle(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "bash", self.dotfiles + "hypr/scripts/gamemode.sh"])

    def on_dock_toggle(self, widget, _):
        if (os.path.exists(self.homeFolder + "/.config/ml4w/settings/dock-disabled")):
            os.remove(self.homeFolder + "/.config/ml4w/settings/dock-disabled")
            subprocess.Popen(["flatpak-spawn", "--host", "bash", self.dotfiles + "nwg-dock-hyprland/launch.sh"])
        else:
            file = open(self.homeFolder + "/.config/ml4w/settings/dock-disabled", "w+")
            subprocess.Popen(["flatpak-spawn", "--host", "killall", "nwg-dock-hyprland"])

    def on_wallpaper_cache_toggle(self, widget, _):
        if (os.path.exists(self.dotfiles + "ml4w/settings/wallpaper_cache")):
            os.remove(self.dotfiles + "ml4w/settings/wallpaper_cache")
        else:
            file = open(self.dotfiles + "ml4w/settings/wallpaper_cache", "w+")

    def on_waybar_toggle(self, widget, _):
        if (os.path.exists(self.homeFolder + "/.config/ml4w/settings/waybar-disabled")):
            os.remove(self.homeFolder + "/.config/ml4w/settings/waybar-disabled")
        else:
            file = open(self.homeFolder + "/.config/ml4w/settings/waybar-disabled", "w+")
        self.reloadWaybar()

    def on_rofi_bordersize(self, widget):
        value = int(widget.get_value())
        text = "* { border-width: " + str(value) + "px; }"
        self.overwriteFile("ml4w/settings/rofi-border.rasi",text)
        self.updateSettingsBash("rofi_bordersize", value)

    def on_blur_radius(self, widget):
        radius = str(int(widget.get_value()))
        sigma = str(int(self.blur_sigma.get_adjustment().get_value()))
        text = radius + "x" + sigma
        self.overwriteFile("ml4w/settings/blur.sh",text)

    def on_blur_sigma(self, widget):
        sigma = str(int(widget.get_value()))
        radius = str(int(self.blur_radius.get_adjustment().get_value()))
        text = radius + "x" + sigma
        self.overwriteFile("ml4w/settings/blur.sh",text)

    def on_waybar_show_appmenu(self, widget, _):
        if widget.get_active():
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
        if widget.get_active():
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"wlr/taskbar"','        "wlr/taskbar",')
            self.updateSettingsBash("waybar_taskbar", True)
        else:
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"wlr/taskbar"','        //"wlr/taskbar",')
            self.updateSettingsBash("waybar_taskbar", False)
        self.reloadWaybar()

    def on_waybar_show_quicklinks(self, widget, _):
        if widget.get_active():
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"group/quicklinks"','        "group/quicklinks",')
            self.updateSettingsBash("waybar_quicklinks", True)
        else:
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"group/quicklinks"','        //"group/quicklinks",')
            self.updateSettingsBash("waybar_quicklinks", False)
        self.reloadWaybar()

    def on_waybar_show_network(self, widget, _):
        if widget.get_active():
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        "network",')
            self.updateSettingsBash("waybar_network", True)
        else:
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"network"','        //"network",')
            self.updateSettingsBash("waybar_network", False)
        self.reloadWaybar()

    def on_waybar_show_window(self, widget, _):
        if widget.get_active():
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        "hyprland/window",')
            self.updateSettingsBash("waybar_window", True)
        else:
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"hyprland/window"','        //"hyprland/window",')
            self.updateSettingsBash("waybar_window", False)
        self.reloadWaybar()

    def on_waybar_show_systray(self, widget, _):
        if widget.get_active():
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        "tray",')
            self.updateSettingsBash("waybar_systray", True)
        else:
            for t in self.waybar_themes:
                self.replaceInFile("waybar/themes/" + t + "/config",'"tray"','        //"tray",')
            self.updateSettingsBash("waybar_systray", False)
        self.reloadWaybar()

    def on_waybar_show_screenlock(self, widget, _):
        if widget.get_active():
            self.replaceInFileCheckpoint("waybar/modules.json", 'group/tools', '"custom/hypridle"', '      "custom/hypridle",')
            self.updateSettingsBash("waybar_screenlock", True)
        else:
            self.replaceInFileCheckpoint("waybar/modules.json", 'group/tools', '"custom/hypridle"', '//      "custom/hypridle",')
            self.updateSettingsBash("waybar_screenlock", False)
        self.reloadWaybar()

    def on_waybar_show_chatgpt(self, widget, _):
        if widget.get_active():
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
        subprocess.Popen(["flatpak-spawn", "--host", "setsid", launch_script, "1>/dev/null" ,"2>&1" "&"])

    # Callback for the app.about action.
    def on_about_action(self, *args):
        about = Adw.AboutDialog(
            application_name="ML4W Settings App",
            developer_name="Stephan Raabe",
            version="2.9.8.4",
            website="https://github.com/mylinuxforwork/dotfiles-settings",
            issue_url="https://github.com/mylinuxforwork/dotfiles-settings/issues",
            support_url="https://github.com/mylinuxforwork/dotfiles-settings/issues",
            copyright="© 2025 Stephan Raabe",
            license_type=Gtk.License.GPL_3_0_ONLY
        )
        about.present(self.props.active_window)

    # Add an application action.
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

# The application's entry point.
def main(version):
    app = DotfilesSettingsApplication()
    return app.run(sys.argv)
