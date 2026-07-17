#!/usr/bin/env bash

RELDIR="$(dirname "$(realpath "$0")")"

#Apply chmod
chmod +x ./fbmenuctl
chmod +x ./fbmenuctl_gen.sh
chmod +x ./fbmenuctl_gui.py

#Move files
sudo mv ./fbmenuctl /bin/fbmenuctl
sudo mv ./fbmenuctl_gen.sh /bin/fbmenuctl_gen.sh
sudo mv ./fbmenuctl_gui.py /usr/libexec/fbmenuctl_gui.py
sudo mkdir -p "$HOME/.local/share/fbmenuctl"
for FILE in "$RELDIR/Categories/"*; do
	mv "$FILE" "$HOME/.local/share/fbmenuctl/$(basename $FILE)"
done
