#!/usr/bin/env bash

#Category Dir
CATDIR="$HOME/.local/share/fbmenuctl/"


#Fluxbox menu file
MENU="$HOME/.fluxbox/menu-fbmenuctl"

#Source directories
DESKDIR="/usr/share/applications/"	#Desktop Files
BINDIR="/bin/"				#Binaries



scrape_categories() {
	echo "[submenu] ($(basename "$1"))" >> "$MENU"
	while IFS= read -r LINE || [ -n "$LINE" ];
	do
		case "$LINE" in
			D::*) #Desktop
				LINE=${LINE#D::}
				local BUFFER=$(grep -m 1 "^Name=" "$DESKDIR$LINE")
				local NAME="${BUFFER#Name=}"
				BUFFER=$(grep -m 1 "^Exec=" "$DESKDIR$LINE")
				local EXEC="${BUFFER#Exec=}"
				EXEC="${EXEC%% %*}"
				echo "[exec] ($NAME) {$EXEC}" >> "$MENU"
				;;
			B::*) #Bin
				echo "[exec] (${LINE#B::}) {xdg-terminal-exec ${LINE#B::}}" >> "$MENU"
				;;
			C::*) #Command
				echo "[exec] (${LINE#C::}) {xdg-terminal-exec ${LINE#C::}}" >> "$MENU"
				;;
			F::*) #Folder
				echo "[exec] (${LINE#F::}) {xdg-open ${LINE#F::}}" >> "$MENU"
				;;
			SC::*) #Subcategory Start
				echo "[submenu] (${LINE#SC::})" >> "$MENU"
				;;
			SE::*) #Subcategorz End
				echo "[end]" >> "$MENU"
				;;
			*)
				echo "$LINE could not be parsed. Perhaps you forgot a prefix?"
				;;
		esac
	done < "$1"
	echo "[end]" >> "$MENU"
}

handle_categories(){
	if [ -f "$CATDIR/Header" ]; then cat "$CATDIR/Header" >> "$MENU"; fi
	for CATEGORY in "$CATDIR"*;
	do
		if [ "$(basename $CATEGORY)" == "Header" ] || [ "$(basename $CATEGORY)" == "Footer" ]; then
			continue
		elif [ -s "$CATEGORY" ]; then
			echo "$CATEGORY located!"
			scrape_categories "$CATEGORY"
		else
			echo "$CATEGORY is empty. Skipping..."
		fi
	done
        if [ -f "$CATDIR/Footer" ]; then cat "$CATDIR/Footer" >> "$MENU"; fi

}

echo "" > "$MENU"
handle_categories
