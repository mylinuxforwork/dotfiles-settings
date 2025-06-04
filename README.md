# ML4W Dotfiles Settings App

Users of the ML4W Dotfiles for Hyprland can use the ML4W Settings App to configure settings of the configuration. 

![image](https://github.com/user-attachments/assets/fb222c31-17a0-40e7-97ca-75017db85b0a)

You can configure the behaviour and modules of the status bar Waybar, appearance options for the application launcher Rofi and many aspects of your Hyprland configuration with configuration variations.

https://github.com/mylinuxforwork/dotfiles/wiki/Configuration-Variations

The ML4W Settings App will be installed with the Dotfiles as Flatpak.

## Installation

Copy the following command into your terminal.

```
bash -c "$(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-settings/master/setup.sh)"
```
> The installation is build with ML4W Packages Installer. https://github.com/mylinuxforwork/packages-installer

## Uninstall

```
flatpak uninstall com.ml4w.settings
```