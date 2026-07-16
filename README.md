# fbmenuctl

---

## Description

**fbmenuctl** is a small menu manager for the Fluxbox WM equipped with a GUI, and a custom way of handling categories. It was a small 4-day project of an amateur developer, so any forking/feedback is very much appreciated, and always welcome!

However- **this utility requires the use of xterm as your default terminal, and Thunar as your default file browser**. Because it hasn't been adapted to use either software of choice. You can edit that in the **fbmenuctl_gen.sh** parser, if you're feeling tinkery.

---

## Features

- Creating categories

- Creating submenus

- Adding files from /usr/share/applications and /bin/ to the menu.

- Adding files and commands to the menu.

- A custom GUI to handle all of that, alongside error handling.

- A custom .fluxbox/menu parser, which does not overwrite the old fluxbox-generate_menu

- An installer

---

## Installation

1) Download the tar.gz. from Releases

2) Open your terminal

3) Type the following commands:

```
cd ~/Downloads/fbmenuctl
./install.sh
```

Note: This will require your sudo password

### Dependencies:

- python

- tkinter

- pathlib

- subprocess

---

## How does it work?

### The categories:

They're stored in **~/.local/share/fbmenuctl** as raw text files without a suffix. Each entry must have a dedicated prefix:

- **D::**    Desktop File (/usr/share/applications)
* **B::**    Bin File (/bin/)
- **F::**    File
- **C::**    Command
- **SC::**    Subcategory Create
- **SE::**    Subcategory End

Anything after :: is then used in the parser, to determine the argument (except for SE::, which is ignored- and used more as a comment for better readability.)

### The Parser

The parser is located within /bin/fbmenuctl_gen.sh, and does the following:

1) Find all of the category files

2) If it's empty, skip it. If it's the header or footer, parse it separately. If neither applies, proceed.

3) Read all of the lines within it.

4) Append them to ~/.fluxbox/menu according to the prefix, and arguments.

Feel free to mod it at any time!

### The UI

Upon typing **fbmenuctl**, you'll be greeted with this GUI:

![](https://i.imgur.com/KxvGjmm.png)

**Left Top-Down Menu**: Select a "From" option (.desktop files, /bin/ files, command,                                             and file)

**Right Top-Down Menu**: Select a category, to which you want to write.

**Left Listbox**: Your selection menu. If you choose a "From" option, that's either File or Command, it transforms itself to a text input.

**+ Button**: Append any selected options to the category.

**- Button**: Remove any selected options from the category.

**^ Button**: Shift any selected options upward.

**v Button**: Shift any selected options downward.

**Right Listbox**: The entries within your category.

**Add Category [Text]**: Create a new category with the [Text] name.

**Remove Category [Selection]**: Select a category using the [Selection], and click a button. That category file should now be deleted.

**Add Subcategory [Text]**: Create a new subcategory within your currently selected category with the [Text] name.

**End Subcategory [Text]**: End the most recent subcategory, the [Text] is fully optional, and serves more as a comment- since it's ignored by the parser.

**Apply**: Applies the changes you have made to the selected category, and calls the parser to immediately apply your changes to the menu itself.

**Storno**: Quits the program.

NOTE: The GUI is **VERY POORLY WRITTEN**.

---

## Uninstalling

 Since there is no uninstaller yet- the removal process is very finicky...

1) Remove **fbmenuctl** from **/bin/**

2) Remove **fbmenuctl_gen.sh** from **/bin/**

3) Remove **fbmenuctl_gui.py** from **/usr/libexec**

4) Remove the entire **~/.local/share/fbmenuctl** folder.

--- 

## Roadmap:

- Create a changes query, so you can change categories mid-editing.

- Make it use your default applications, instead of the only ones supported.

- Add an uninstaller

- Who knows?
