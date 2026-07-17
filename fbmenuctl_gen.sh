#!/usr/bin/env bash

#Category Dir
CATDIR="$HOME/.local/share/fbmenuctl/"


#Fluxbox menu file
MENU="$HOME/.fluxbox/menu"

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
				echo "[exec] (${LINE#B::}) {xterm -e ${LINE#B::}}" >> "$MENU"
				;;
			C::*) #Command
				echo "[exec] (${LINE#C::}) {xterm -e ${LINE#C::}}" >> "$MENU"
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
	if [ -f "$CATDIR/1Header" ]; then cat "$CATDIR/1Header" >> "$MENU"; fi
	if [ -f "$CATDIR/ZFooter" ]; then cat "$CATDIR/ZFooter" >> "$MENU"; fi
	for CATEGORY in "$CATDIR"*;
	do
		if [ "$(basename "$CATEGORY")" == "1Header" ] || [ "$(basename "$CATEGORY")" == "ZFooter" ]; then
			continue
		elif [ -s "$CATEGORY" ]; then
			echo "$CATEGORY located!"
			scrape_categories "$CATEGORY"
		else
			echo "$CATEGORY is empty. Skipping..."
		fi
	done
}

echo "" > "$MENU"
handle_categories
