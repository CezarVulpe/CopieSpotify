import socket
from admin import Admin
from users import open_user_window

def start_server(root, text_area_admin, host='0.0.0.0', port=12345):
    admin = Admin()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[SERVER] Listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    data = conn.recv(1024).decode()
                    print(f"[SERVER] Received: {data}")

                    if data.startswith("add_user:"):
                        username = data.split(":", 1)[1]
                        user = User(username, 25, "Unknown")
                        admin.add_user(user)

                        # Actualizare GUI (foloseste `after` pentru thread safety)
                        if text_area_admin:
                            text_area_admin.after(0, text_area_admin.insert, tk.END, f"[REMOTE] User '{username}' added.\n")
                        if root:
                            root.after(0, open_user_window, root, username)

                        conn.send(f"User '{username}' added.".encode())
                    else:
                        conn.send(b"Invalid command.")
                except Exception as e:
                    conn.send(f"Error: {e}".encode())
