import socket
import tkinter as tk
from users import open_user_window, User

def add_user(username, host="192.168.18.138", port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(f"add_user:{username}".encode())

        response = s.recv(1024).decode()
        print(f"[CLIENT] Server response: {response}")

    return username  # Returnăm numele pentru fereastra locală

if __name__ == "__main__":
    # Trimite cererea de adăugare la admin/server
    username = add_user("aaa")

    # Deschide fereastra locală pentru utilizator (client GUI)
    root = tk.Tk()
    root.withdraw()  # ascundem fereastra principală

    open_user_window(root, username, is_remote=True)

    root.mainloop()
