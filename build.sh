#!/bin/bash
rm -rf ~/tmp
mkdir ~/tmp
cp -r . ~/tmp
rm -rf ~/tmp/.git
rm -rf ~/tmp/release
rm -rf ~/tmp/screenshots
rm ~/tmp/.gitignore
rm ~/tmp/build.sh
rm ~/tmp/install.sh
cd ..
ARCH=x86_64 appimagetool tmp
echo ":: AppImage created"
cp ML4W_Dotfiles_Settings-x86_64.AppImage ~/.ml4w-hyprland/dotfiles/share/apps/com.ml4w.dotfilessettings
echo ":: AppImage copied to ~/.ml4w-hyprland/dotfiles/share/apps/"
