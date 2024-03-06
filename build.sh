#!/bin/bash
cp usr/bin/restore.py ~/dotfiles-versions/dotfiles/.install/
echo ":: restore.py copied to ~/dotfiles-versions/dotfiles/.install/"
cd ..
ARCH=x86_64 appimagetool ml4w-dotfiles-settings
echo ":: AppImage created"
cp ML4W_Dotfiles_Settings-x86_64.AppImage ~/dotfiles-versions/dotfiles/apps/
echo ":: AppImage copied to ~/dotfiles-versions/dotfiles/apps/"
