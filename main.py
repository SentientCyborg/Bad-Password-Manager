import pyperclip
import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
from ctypes import windll

# makes everything sharp on certain monitors -- comment this out if it makes things worse
windll.shcore.SetProcessDpiAwareness(1)

BG_COLOR = "#F2F2F2"
# "#F5EDDC"
x = 5
y = 5
email = "name@email.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# This is a refactor of the password generator built on Day 5

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_nums = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pass_letters + pass_nums + pass_symbols
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    site = web_entry.get()
    name = user_entry.get()
    password = pass_entry.get()

    if len(site) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave empty fields.")
    else:
        is_ok = messagebox.askokcancel(title=site, message=f"These are the details entered: \nUser: {name}"
                                                   f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open("data.txt", "a") as f:
                phrase = f"{site} | {name} | {password}\n"
                f.write(phrase)
            reset_entries()


def reset_entries():
    web_entry.delete(0, tk.END)
    user_entry.config(text=email)
    pass_entry.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)

canvas = tk.Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)  # x, y, image
canvas.grid(row=0, column=1)


# labels
web_label = tk.Label(text="Website:", bg=BG_COLOR, font="bold")
web_label.grid(row=1, column=0)

user_label = tk.Label(text="Email/Username:", bg=BG_COLOR, font="bold")
user_label.grid(row=2, column=0)

pass_label = tk.Label(text="Password:", bg=BG_COLOR, font="bold")
pass_label.grid(row=3, column=0)


# Entries
web_entry = tk.Entry()
web_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
web_entry.focus()

user_entry = tk.Entry()
user_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
user_entry.insert(0, email)  # index where to insert text

pass_entry = tk.Entry()
pass_entry.grid(row=3, column=1, sticky="EW")


# Buttons
pass_button = tk.Button(text="Generate Password", font="bold", command=generate_password)
pass_button.grid(row=3, column=2, sticky="EW")

add_button = tk.Button(text="Add", font="bold", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
