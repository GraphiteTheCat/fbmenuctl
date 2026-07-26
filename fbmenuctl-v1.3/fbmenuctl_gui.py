import tkinter as tk
from tkinter import ttk as ttk
import pathlib
from pathlib import Path
import subprocess

# VARIABLES

from_list = ["/usr/share/applications", "/bin/", "File", "Command"]
from_var = pathlib.Path("/usr/share/applications")
to_var = pathlib.Path(f"{Path.home()}/.local/share/fbmenuctl")
to_list = []

cat=""
cat_content_list = []
cat_content_prefix = ""


# LOGIC

def reload_to():
	global to_sel

	to_sel.delete(0, tk.END)
	for line in cat_content_list:
		to_sel.insert(tk.END, line)
	return

def apply():
	global to_dir
	global to_list
	global to_var
	global err_dis
	path = pathlib.Path(f"{to_var}/{to_dir.get()}")
	if not path.exists():
		err_dis.config(text="Category does not exist!")
		return
	elif not path.is_file():
		err_dis.config(text="Category not selected!")
		return

	with path.open("w") as file:
		for entry in cat_content_list:
			file.write(f"{entry}\n")
	subprocess.run(["/bin/fbmenuctl_gen.sh"])
	return

def append_subcat():
	global subadd_entry
	global cat_content_list
	global to_dir
	global err_dis

	if not subadd_entry.get():
		err_dis.config(text="Subcategory name not provided!")
		return
	if not to_dir.get():
		err_dis.config(text="Category not provided!")
		return

	cat_content_list.append(f"SC::{subadd_entry.get()}")
	reload_to()
	return

def append_subcat_end():
	global subend_entry
	global cat_content_list

	cat_content_list.append(f"SE::{subend_entry.get()}")
	reload_to()
	return

def append_from_to():
	global from_sel
	global from_text
	global cat_content_list
	global to_sel
	global from_dir
	global err_dis

	if (not from_sel.curselection() and from_dir.get() not in ["File", "Command"]) and not to_dir.get():
		err_dis.config(text="No FROM element and Category selected!")
		return
	elif not from_sel.curselection() and from_dir.get() not in ["File", "Command"]:
		err_dis.config(text="No FROM element selected!")
		return
	elif not from_text.get("1.0", "end-1c") and from_dir.get() in ["File", "Command"]:
		err_dis.config(text="FROM text file is empty!")
		return
	elif not to_dir.get():
		err_dis.config(text="No Category selected!")
		return

	if from_dir.get() not in ["File", "Command"]:
		for selection in from_sel.curselection():
			cat_content_list.append(f"{cat_content_prefix}{from_sel.get(selection)}")
	else:
		cat_content_list.append(f"{cat_content_prefix}{from_text.get("1.0", "end-1c")}")
	reload_to()
	return

def remove_element_to():
	global to_sel
	global cat_content_list
	global err_dis

	if not to_sel.curselection():
		err_dis.config(text="No element selected!")
		return

	for selection in to_sel.curselection():
		cat_content_list.pop(cat_content_list.index(to_sel.get(selection)))
	reload_to()
	return

def move_to_up():
	global to_sel
	global cat_content_list
	global err_dis

	if not to_sel.curselection():
		err_dis.config(text="No element selected!")
		return

	for selection in to_sel.curselection():
		if selection == 0:
			err_dis.config(text="Cannot move first element upwards!")
		old_index = cat_content_list.index(to_sel.get(selection))
		cat_content_list.insert(old_index - 1, cat_content_list[selection])
		cat_content_list.pop(old_index + 1)
	reload_to()
	return

def move_to_down():
	global to_sel
	global cat_content_list
	global err_dis

	if not to_sel.curselection():
		err_dis.config(text="No element selected!")
		return

	for selection in to_sel.curselection():
		if selection == len(cat_content_list) - 1:
			err_dis.config(text="Cannot move last element down!")
			continue
		old_index = cat_content_list.index(to_sel.get(selection))
		cat_content_list.insert(old_index + 2, cat_content_list[selection])
		cat_content_list.pop(old_index)
	reload_to()
	return

def load_cat(event):
	global cat
	global cat_content_list
	global to_dir
	global to_var
	global to_sel
	global err_dis

	to_sel.delete(0, tk.END)
	cat_content_list=[]
	cat = f"{to_var}/{to_dir.get()}"
	if not pathlib.Path(cat).exists():
		err_dis.config(text="Category does not exist!")
		return
	with open(cat) as file:
		for line in file:
			cat_content_list.append(line.strip())
			to_sel.insert(tk.END, line.strip())
	return

def load_catfiles():
	global to_dir
	global to_var
	global catrem_cbox
	global to_list

	to_sel.delete(0, tk.END)
	to_list = []

	for file in to_var.iterdir():
		if file.is_file() and file.name not in ["Header", "Footer"]:
			to_list.append(file.name)
	to_dir.config(values=to_list)
	catrem_cbox.config(values=to_list)
	return

def append_category():
	global catadd_entry
	global to_var
	global err_dis

	if not catadd_entry.get():
		err_dis.config(text="Category name not provided!")
		return

	path = pathlib.Path(f"{to_var}/{catadd_entry.get()}")
	if not path.exists():
		path.touch()
		load_catfiles()
		catadd_entry.delete(0, tk.END)
	return

def remove_category():
	global catrem_cbox
	global to_var
	global err_dis

	if not catrem_cbox.get():
		err_dis.config(text="Category not provided!")
		return

	path = pathlib.Path(f"{to_var}/{catrem_cbox.get()}")
	if not path.exists():
		err_dis.config(text="Category does not exist!")
		return
	path.unlink()
	load_catfiles()
	return

def handle_from(value):
	global from_sel
	global from_entry

	if value not in ["File", "Command"]:
		from_text.grid_forget()
		from_sel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
	else:
		from_sel.grid_forget()
		from_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
	return

def load_from(event):
	global from_sel
	global from_dir
	value = from_dir.get()
	handle_from(value)
	from_sel.delete(0, tk.END)
	if value not in ["File", "Command"]:
		path = pathlib.Path(value)
		for file in path.iterdir():
			if file.is_file():
				from_sel.insert(tk.END, file.name)
	handle_prefix(value)
	return

def handle_prefix(selection):
	global cat_content_prefix

	if selection == "/usr/share/applications":
		cat_content_prefix="D::"
	elif selection == "/bin/":
		cat_content_prefix="B::"
	elif selection == "File":
		cat_content_prefix="F::"
	elif selection == "Command":
		cat_content_prefix="C::"

# GUI

window = tk.Tk()
window.geometry("500x450")
window.title("fbmenuctl")

selection=tk.Frame(window)
selection.columnconfigure(0, weight=4, uniform="man")
selection.columnconfigure(1, weight=1, uniform="man")
selection.columnconfigure(2, weight=4, uniform="man")
selection.pack(fill=tk.X, padx=10, pady=5)

manipulation = tk.Frame(window, relief=tk.RIDGE, bd=3, bg="white", height=200)
manipulation.columnconfigure(0, weight=4, uniform="man")
manipulation.columnconfigure(1, weight=1, uniform="man")
manipulation.columnconfigure(2, weight=4, uniform="man")
manipulation.rowconfigure(0, weight=1, uniform="man")
manipulation.grid_propagate(False)
manipulation.pack(fill=tk.X, padx=10, pady=5)

man_buttons = tk.Frame(manipulation)
man_buttons.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
man_buttons.columnconfigure(0, weight=1, uniform="man_btn")
man_buttons.rowconfigure(0, weight=1, uniform="man_btn")
man_buttons.rowconfigure(1, weight=1, uniform="man_btn")
man_buttons.rowconfigure(2, weight=1, uniform="man_btn")
man_buttons.rowconfigure(3, weight=1, uniform="man_btn")

button_add = tk.Button(man_buttons, text="+", command=append_from_to)
button_add.grid(row=0, column=0, sticky="nsew")

button_remove = tk.Button(man_buttons, text="-", command=remove_element_to)
button_remove.grid(row=1, column=0, sticky="nsew")

button_move_up = tk.Button(man_buttons, text="^", command=move_to_up)
button_move_up.grid(row=2, column=0, sticky="nsew")

button_move_down = tk.Button(man_buttons, text="v", command=move_to_down)
button_move_down.grid(row=3, column=0, sticky="nsew")

from_sel = tk.Listbox(manipulation, selectmode=tk.MULTIPLE)
from_text = tk.Text(manipulation)

from_dir = ttk.Combobox(selection, values=from_list)
from_dir.grid(row=0, column=0, sticky="nsew")
from_dir.bind("<<ComboboxSelected>>", load_from)

to_sel = tk.Listbox(manipulation, selectmode=tk.EXTENDED)
to_sel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

to_dir = ttk.Combobox(selection, values=to_list)
to_dir.grid(row=0, column=2, sticky="nsew")
to_dir.bind("<<ComboboxSelected>>", load_cat)

catman = tk.Frame(window, relief=tk.RIDGE, bd=3, bg="white", height=50)
catman.rowconfigure(0, weight=1, uniform="cm")
catman.rowconfigure(1, weight=1, uniform="cm")
catman.columnconfigure(0, weight=1, uniform="cm")
catman.columnconfigure(1, weight=4, uniform="cm")
catman.grid_propagate(False)
catman.pack(fill=tk.X, padx=10, pady=5)

catadd_btn = tk.Button(catman, text="Add category", font=("Calibri", 7), command=append_category)
catadd_btn.grid(row=0, column=0, sticky="nsew")

catadd_entry = tk.Entry(catman, font=("Calibri", 7))
catadd_entry.grid(row=0, column=1, sticky="nsew")

catrem_btn = tk.Button(catman, text="Remove category", font=("Calibri", 7), command=remove_category)
catrem_btn.grid(row=1, column=0, sticky="nsew")

catrem_cbox = ttk.Combobox(catman)
catrem_cbox.grid(row=1, column=1, sticky="nsew")


subcat = tk.Frame(window, relief=tk.RIDGE, bd=3, bg="white", height=50)
subcat.rowconfigure(0, weight=1, uniform="sc")
subcat.rowconfigure(1, weight=1, uniform="sc")
subcat.columnconfigure(0, weight=1, uniform="sc")
subcat.columnconfigure(1, weight=4, uniform="sc")
subcat.grid_propagate(False)
subcat.pack(fill=tk.X, padx=10, pady=5)

subadd_btn = tk.Button(subcat, text="Add subcategory", font=("Calibri", 7), command=append_subcat)
subadd_btn.grid(row=0, column=0, sticky="nsew")

subadd_entry = tk.Entry(subcat, font=("Calibri", 7))
subadd_entry.grid(row=0, column=1, sticky="nsew")

subend_btn = tk.Button(subcat, text="End subcategory", font=("Calibri", 7), command=append_subcat_end)
subend_btn.grid(row=1, column=0, sticky="nsew")

subend_entry = tk.Entry(subcat, font=("Calibri", 7))
subend_entry.grid(row=1, column=1, sticky="nsew")

err_dis = tk.Label(window, fg="red")
err_dis.pack(pady=5)

apply_btn = tk.Button(window, text="Apply", command=apply, height=1)
apply_btn.pack(padx=10, pady=0)

storno_btn = tk.Button(window, text="Storno", command=exit, height=1)
storno_btn.pack(padx=10, pady=0)

load_catfiles()
window.mainloop()
