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

@Gtk.Template(resource_path='/com/ml4w/settings/window.ui')
class DotfilesSettingsWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'Ml4wSettingsWindow'

    waybar_show_appmenu = Gtk.Template.Child()
    waybar_show_taskbar = Gtk.Template.Child()
    waybar_show_quicklinks = Gtk.Template.Child()
    waybar_show_network = Gtk.Template.Child()
    waybar_show_chatgpt = Gtk.Template.Child()
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
    open_quicklinks = Gtk.Template.Child()
    open_wallpaper_effects = Gtk.Template.Child()
    open_waybar_folder = Gtk.Template.Child()
    open_timeformatspecifications = Gtk.Template.Child()
    restart_hypridle = Gtk.Template.Child()
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
    hypridle_hyprlock = Gtk.Template.Child()
    hypridle_dpms = Gtk.Template.Child()
    hypridle_suspend = Gtk.Template.Child()
    blur_radius = Gtk.Template.Child()
    blur_sigma = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
