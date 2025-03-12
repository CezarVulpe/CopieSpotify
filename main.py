import tkinter as tk
from tkinter import scrolledtext
from users import open_user_window, User
from admin import Admin  # Assuming you move Admin to a separate file

# Initialize the Admin singleton
admin = Admin()

# Initialize main admin window
root = tk.Tk()
root.title("Admin Panel")
root.geometry("400x300")

# Input field for admin
entry_admin = tk.Entry(root, width=40)
entry_admin.pack(pady=10)

# Function to add user
def add_user():
    username = entry_admin.get().strip()
    if username:
        user = User(username, 25, "Unknown")  # Example data
        admin.add_user(user)
        open_user_window(root, username)
        text_area_admin.insert(tk.END, f"User '{username}' added.\n")
    entry_admin.delete(0, tk.END)

# Add user button
add_user_button = tk.Button(root, text="Add User", command=add_user)
add_user_button.pack()

# Text area for admin logs
text_area_admin = scrolledtext.ScrolledText(root, width=40, height=10)
text_area_admin.pack(pady=10)

# Run the app
root.mainloop()
