import hashlib
import os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image

def hash_word(word, hash_type):
    if hash_type == 'md5':
        return hashlib.md5(word.encode()).hexdigest()
    elif hash_type == 'sha1':
        return hashlib.sha1(word.encode()).hexdigest()
    elif hash_type == 'sha224':
        return hashlib.sha224(word.encode()).hexdigest()
    elif hash_type == 'sha256':
        return hashlib.sha256(word.encode()).hexdigest()
    elif hash_type == 'sha384':
        return hashlib.sha384(word.encode()).hexdigest()
    elif hash_type == 'sha512':
        return hashlib.sha512(word.encode()).hexdigest()
    elif hash_type == 'sha3_224':
        return hashlib.sha3_224(word.encode()).hexdigest()
    elif hash_type == 'sha3_256':
        return hashlib.sha3_256(word.encode()).hexdigest()
    elif hash_type == 'sha3_384':
        return hashlib.sha3_384(word.encode()).hexdigest()
    elif hash_type == 'sha3_512':
        return hashlib.sha3_512(word.encode()).hexdigest()
    else:
        print("Invalid hash type")
        return None

def select_hash_type(hash_type):
    global selected_hash_type
    global hash_buttons
    selected_hash_type = hash_type
    for button in hash_buttons:
        if button['text'] == selected_hash_type:
            button.config(relief=SUNKEN)
        else:
            button.config(relief=RAISED)

def browse_file():
    global dictionary_file
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
    if filename:
        dictionary_file = filename
        file_label.config(text=os.path.basename(dictionary_file))

def compare_hashes():
    global dictionary_file
    global selected_hash_type
    global encoding_var
    if not dictionary_file:
        output_text.config(text="Please select a dictionary file.")
        return
    if not selected_hash_type:
        output_text.config(text="Please select a hash type.")
        return
    target_hash = target_hash_entry.get()
    encoding = encoding_var.get()
    try:
        with open(dictionary_file, 'r', encoding=encoding) as f:
            dictionary = f.read().splitlines()
    except UnicodeDecodeError:
        output_text.config(text="Unable to decode the dictionary file using the specified encoding.")
        return
    found = False
    progress_bar['maximum'] = len(dictionary)
    for i, word in enumerate(dictionary):
        word_hash = hash_word(word.strip(), selected_hash_type)
        if word_hash == target_hash:
            output_text.config(text="Success! The word '{}' hashes to the target hash.".format(word))
            found = True
            break
        progress_bar['value'] = i + 1
        root.update_idletasks()
    if not found:
        output_text.config(text="No match found in the dictionary.")

def show_info():
    info_window = Toplevel(root)
    info_window.title("Information")
    info_window.geometry("300x100")
    info_label = Label(info_window, text="Created by: Deckcard23\nVersion: 1.0\nTwitter: @rickdeckard23\ndeckcard23.com\email:info@deckcard23.com")
    info_label.pack()


root = Tk()
root.title("Hash Cracker")
root.geometry("600x400")

logo_image = ImageTk.PhotoImage(Image.open("logo_deckcard23.jpg"))
logo_label = Label(image=logo_image)
logo_label.pack()

hash_types_frame = Frame(root)
hash_types_frame.pack()

hash_types = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
hash_buttons = []
for hash_type in hash_types:
    button = Button(hash_types_frame, text=hash_type, command=lambda ht=hash_type: select_hash_type(ht))
    button.pack(side=LEFT)
    hash_buttons.append(button)

file_label = Label(root, text="\nSelect wordlist to attack:")
file_label.pack()

target_hash_entry = Entry(root)
target_hash_entry.pack()

browse_button = Button(root, text="Browse", command=browse_file)
browse_button.pack()

file_label = Label(root, text="\nHash to decrypt:")
file_label.pack()

target_hash_entry = Entry(root)
target_hash_entry.pack()

encoding_label = Label(root, text="\nEncoding:")
encoding_label.pack()

encoding_var = StringVar(root)
encoding_var.set("utf-8")
encoding_options = ["utf-8", "iso-8859-1", "windows-1252"]
encoding_optionmenu = OptionMenu(root, encoding_var, *encoding_options)
encoding_optionmenu.pack()

compare_button = Button(root, text="Start Cracking", command=compare_hashes)
compare_button.pack()

progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.pack()

output_text = Label(root, text="")
output_text.pack()

menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Info", command=show_info)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

dictionary_file = None
selected_hash_type = None

root.mainloop()
