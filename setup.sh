#!/bin/bash
# Created with Packages Installer 0.1
# https://github.com/mylinuxforwork/packages-installer

clear
# Seperator
_sep() {
	echo "----------------------------------------------------"
}

# Spacer
_space() {
	echo
}

# Default
assumeyes=1
cmdoutput="/dev/null 2>&1"

# Options
while getopts y?h?o? option
do
    case "${option}"
        in
        y|\?)
	        assumeyes=0
        	;;
        o|\?)
	        cmdoutput="echo"
        	;;
        h|\?)
		echo "Created with Packages Manager 0.1"
		echo
		echo "Usage:"
		echo "-y Skip confirmation"
		echo "-o Show installation command outputs"
		echo "-h Help"
		exit
        	;;
    esac
done

# Variables


# Is installed
_isInstalled_flatpak() {
	package="$1"
	check=$(flatpak info ${package})
	if [[ $check == *"ID:"* ]]; then
	  	echo 0
	else
		echo 1
	fi
}

# Add flathub remote
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo


_isInstalled_flatpak() {
	package="$1"
	check=$(flatpak info ${package})
	if [[ $check == *"ID:"* ]]; then
	  	echo 0
	else
		echo 1
	fi
}

# Add flathub remote
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo


# Header
_sep
echo "Setup ML4W Dotfiles Settings"
echo "Remote Installation of Flatpak"
_space
echo "Created with Packages Manager 0.1"
_sep
_space
echo "IMPORTANT: Please make sure that your system is updated before starting the installation."
_space

# Confirm Start
if [ $assumeyes == 1 ]; then
	while true; do
		read -p "DO YOU WANT TO START THE INSTALLATION NOW? (Yy/Nn): " yn
		case $yn in
		    [Yy]*)
		        break
		        ;;
		    [Nn]*)
		        echo ":: Installation canceled"
		        exit
		        break
		        ;;
		    *)
		        echo ":: Please answer yes or no."
		        ;;
		esac
	done
fi

# sudo permissions
sudo -v
_space

# Packages
if [ ! -d $HOME/.cache ]; then
	mkdir -p $HOME/.cache
fi
wget -q -P "$HOME/.cache" "https://github.com/mylinuxforwork/dotfiles-settings/releases/latest/download/com.ml4w.settings.flatpak"
cd "$HOME/.cache"
echo ":: Installing com.ml4w.settings.flatpak"
eval "flatpak --user -y --reinstall install com.ml4w.settings.flatpak > $cmdoutput"
rm "$HOME/.cache/com.ml4w.settings.flatpak"


_space

# Success Message
_sep
echo "DONE!"
_sep