import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_new_password():
    """Generates a random password based on user's desired length."""
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("Oops!", "Please enter a positive number for password length.")
            return

        all_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(all_characters) for _ in range(length))
        password_display_label.config(text=password) # Display the generated password.
    except ValueError:
        messagebox.showerror("Uh-oh!", "Please enter a valid whole number for the length.")


app = tk.Tk()
app.title("Your Friendly Password Creator")
app.geometry("400x250") # A cozy size for our window
app.config(bg="#1A1A1A") # Dark background for the black theme


length_label = tk.Label(app, text="How long should your awesome password be?",
                        bg="#1A1A1A", fg="#ADD8E6", font=("Arial", 12))
length_label.pack(pady=10)

length_entry = tk.Entry(app, width=10, font=("Arial", 14), bd=2, relief="flat",
                        bg="#333333", fg="#ADD8E6", insertbackground="#ADD8E6")
length_entry.pack(pady=5)
length_entry.focus_set() # Ready for typing!

#Generate passsword
generate_button = tk.Button(app, text="Conjure My Password!", command=generate_new_password,
                            bg="#005B96", fg="white", font=("Arial", 12, "bold"),
                            relief="raised", bd=3, activebackground="#007ACC", activeforeground="white")
generate_button.pack(pady=15)

# Where your new password will appear
password_label_heading = tk.Label(app, text="Here's your secret key:",
                                   bg="#1A1A1A", fg="#ADD8E6", font=("Arial", 11, "italic"))
password_label_heading.pack()

password_display_label = tk.Label(app, text="", wraplength=350, justify="center",
                                  bg="#2C2C2C", fg="#F0F8FF", font=("Courier New", 14, "bold"),
                                  relief="sunken", bd=2, padx=10, pady=10)
password_display_label.pack(pady=10, padx=20, fill="x")

app.mainloop() 
