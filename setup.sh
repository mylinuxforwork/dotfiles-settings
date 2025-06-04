#!/bin/bash

# ----------------------------------------------------------
# Flatpak Information
# ----------------------------------------------------------

runtime="org.gnome.Platform/x86_64/47"
app="com.ml4w.settings"
download="https://github.com/mylinuxforwork/dotfiles-settings/releases/latest/download/$app.flatpak"

# ----------------------------------------------------------
# Check if command exists
# ----------------------------------------------------------

_commandExists() {
    package="$1"
    if ! type $package >/dev/null 2>&1; then
        echo 1
    else
        echo 0
    fi
}

# ----------------------------------------------------------
# Check if app is already installed
# ----------------------------------------------------------

_checkFlatpakAppExists() {
	app="$1"
	flatpak_output=$(flatpak info $runtime)
	if [[ $flatpak_output == *"ID:"* ]]; then
	  	echo 0
	else
		echo 1
	fi
}

# ----------------------------------------------------------
# Check if flatpak is already installed
# ----------------------------------------------------------

if [ "$(_commandExists "flatpak")" == "1" ]; then
	echo "ERROR: Please install flatpak first."
	exit
fi

# ----------------------------------------------------------
# Adding flathub remote
# ----------------------------------------------------------

flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# ----------------------------------------------------------
# Check for runtime
# ----------------------------------------------------------

if [ "$(_checkFlatpakAppExists "$runtime")" == "1" ]; then
	echo
	echo ":: Installing runtime $runtime"
	sudo flatpak -y install $runtime
fi

# ----------------------------------------------------------
# Download app
# ----------------------------------------------------------

echo
echo ":: Downloading $app"
if [ ! -d "$HOME/.cache" ]; then
	mkdir -p "$HOME/.cache"
fi
if [ -f "$HOME/.cache/$app.flatpak" ]; then
	rm "$HOME/.cache/$app.flatpak"
fi
wget -P "$HOME/.cache" "$download"
if [ ! -f "$HOME/.cache/$app.flatpak" ]; then
	echo "ERROR: Download of $app.flatpak failed."
	exit
fi
# ----------------------------------------------------------
# Install app
# ----------------------------------------------------------

cd "$HOME/.cache"
flatpak --user -y --reinstall install $app.flatpak

# ----------------------------------------------------------
# Cleanup
# ----------------------------------------------------------

if [ -f "$HOME/.cache/$app.flatpak" ]; then
	rm "$HOME/.cache/$app.flatpak"
fi

# ----------------------------------------------------------
# Finishing up
# ----------------------------------------------------------

echo
echo ":: Setup complete. Run the app with flatpak run $app"
