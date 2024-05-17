import os
import configparser
from tkinter import Tk, filedialog, Listbox, Label, END, messagebox, Frame
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def save_directory(directory):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Directory': directory}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_directory():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT'].get('Directory', '')

def directory_exists(directory):
    return os.path.exists(directory) and os.path.isdir(directory)

def list_txt_files(base_directory):
    txt_files = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        folder_path = os.path.join(base_directory, letter)
        print(f"Checking folder: {folder_path}")  # Debug message
        if directory_exists(folder_path):
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.txt'):
                        full_path = os.path.join(root, file)
                        txt_files.append(full_path)
                        print(f"Found text file: {full_path}")
        else:
            print(f"Folder does not exist: {folder_path}")
    return txt_files

def read_key_words():
    try:
        with open('KeyList.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        messagebox.showerror("Error", "KeyList.txt not found")
        return []

def create_index(files, key_words):
    index = {word: 0 for word in key_words}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            for word in key_words:
                index[word] += content.count(word)
    return index

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_directory(directory)
        directory_label.config(text=directory)
        update_file_list()

def update_file_list():
    base_directory = load_directory()
    print(f"Base directory: {base_directory}")  # Debug message
    if base_directory and directory_exists(base_directory):
        txt_files = list_txt_files(base_directory)
        print(f"Total text files found: {len(txt_files)}")  # Debug message
        files_listbox.delete(0, END)
        for file in txt_files:
            files_listbox.insert(END, file)
            print(f"Inserted text file: {file}")  # Debug message
    else:
        print(f"Base directory does not exist or not set: {base_directory}")

def show_statistics():
    selected_indices = key_words_listbox.curselection()
    selected_key_words = [key_words_listbox.get(i) for i in selected_indices]
    if not selected_key_words:
        messagebox.showwarning("Warning", "No key words selected")
        return

    base_directory = load_directory()
    txt_files = list_txt_files(base_directory)
    key_words = read_key_words()
    index = create_index(txt_files, key_words)

    statistics = []
    for word in selected_key_words:
        count = sum(index[word] for word in selected_key_words)
        statistics.append(f"{word}: {index[word]}")

    statistics_message = "\n".join(statistics)
    messagebox.showinfo("Statistics", statistics_message)

root = Tk()
root.title("Key Word Indexer")
root.geometry("800x800")
root.configure(bg="#BFE8DF")

style = ttk.Style()
style.configure("TButton", foreground="white", background="#00A67E", borderwidth=0)
style.map("TButton",
          background=[('active', '#009E6E'), ('pressed', '#007A56')],
          foreground=[('disabled', '#ffffff')])

main_frame = Frame(root, padx=20, pady=20, bg="#BFE8DF")
main_frame.pack(fill="both", expand=True)

directory_label = ttk.Label(main_frame, text="Select Directory:", background="#BFE8DF")
directory_label.pack(pady=10)
browse_button = ttk.Button(main_frame, text="Browse", style="success.TButton", command=browse_directory)
browse_button.pack(pady=10)

files_label = ttk.Label(main_frame, text="Text Files:", background="#BFE8DF")
files_label.pack(pady=10)
files_listbox = Listbox(main_frame, width=100, height=15)
files_listbox.pack(pady=10)

key_words_label = ttk.Label(main_frame, text="Key Words:", background="#BFE8DF")
key_words_label.pack(pady=10)
key_words_listbox = Listbox(main_frame, selectmode='multiple', width=50, height=15, highlightbackground="#00A67E", highlightthickness=1, selectbackground="#00A67E", activestyle='none')
key_words_listbox.pack(pady=10)

key_words = read_key_words()
for word in key_words:
    key_words_listbox.insert(END, word)

show_statistics_button = ttk.Button(main_frame, text="Show Statistics", style="success.TButton", command=show_statistics)
show_statistics_button.pack(pady=10)

saved_directory = load_directory()
if saved_directory:
    directory_label.config(text=saved_directory)
    update_file_list()

root.mainloop()
