import pyperclip
import json
import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
from ctypes import windll

# makes everything sharp on certain monitors -- comment the line below if it makes things worse
windll.shcore.SetProcessDpiAwareness(1)

BG_COLOR = "#F2F2F2"
default_user = "name@email.com"
data_json = "data.json"


def generate_password():
    """Generates a random password using the available characters"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '@']

    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_nums = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pass_letters + pass_nums + pass_symbols
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    """Saves the password entry to a json file."""
    site = web_entry.get().lower()
    password = pass_entry.get()
    new_data = {
        site: {
            "username": default_user,
            "password": password,
        }
    }

    if len(site) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave empty fields.")
    else:
        try:
            with open(data_json, "r") as data_file:
                data = json.load(data_file)
        except(FileNotFoundError, json.decoder.JSONDecodeError):
            with open(data_json, "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open(data_json, "w") as data_file:
                json.dump(data, data_file, indent=4)
    reset_entries()


def search():
    """Looks for the entered website in the json file."""
    site = web_entry.get().lower()
    if len(site) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a site name.")
    else:
        try:
            with open(data_json) as data_file:
                data = json.load(data_file)
        except(FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showerror(title="Oops", message=f"Cannot find '{data_json}'.")
        else:
            if site in data:
                user = data[site]['username']
                password = data[site]['password']
                messagebox.showinfo(title=site, message=f"Username:  {user}\nPassword:  {password}")
                pyperclip.copy(password)
            else:
                messagebox.showerror(title="Oops", message="Site not found.")
    reset_entries()


def reset_entries():
    """Sets all the entry values back to the default"""
    web_entry.delete(0, tk.END)
    user_entry.config(text=default_user)
    pass_entry.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)

canvas = tk.Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_img = tk.PhotoImage(file="images/logo.png")
canvas.create_image(100, 100, image=logo_img)  # x, y, image
canvas.grid(row=0, column=1)


# labels
web_label = tk.Label(text="Website:", bg=BG_COLOR, font="bold")
web_label.grid(row=1, column=0)

user_label = tk.Label(text="Username:", bg=BG_COLOR, font="bold")
user_label.grid(row=2, column=0)

pass_label = tk.Label(text="Password:", bg=BG_COLOR, font="bold")
pass_label.grid(row=3, column=0)


# Entries
web_entry = tk.Entry()
web_entry.grid(row=1, column=1, sticky="EW")
web_entry.focus()

user_entry = tk.Entry()
user_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
user_entry.insert(0, default_user)  # index where to insert text

pass_entry = tk.Entry()
pass_entry.grid(row=3, column=1, sticky="EW")


# Buttons
pass_button = tk.Button(text="Generate Password", font="bold", command=generate_password)
pass_button.grid(row=3, column=2, sticky="EW")

add_button = tk.Button(text="Save", font="bold", fg='red', width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=5, sticky="EW")

search_button = tk.Button(text="Search", font="bold", fg="white", bg="blue", command=search)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
