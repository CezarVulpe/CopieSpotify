import socket
import os
from admin import Admin

def start_server(host='0.0.0.0', port=12345):
    admin = Admin()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[SERVER] Listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            print(f"[SERVER] Connection from {addr}")
            with conn:
                data = conn.recv(1024).decode()
                print(f"[SERVER] Received: {data}")

                if data.startswith("request_song:"):
                    try:
                        index = int(data.split(":")[1]) - 1
                        if 0 <= index < len(admin.songs):
                            song_path = admin.songs[index]
                            if not os.path.isfile(song_path):
                                conn.send(b"ERROR: File not found")
                                continue

                            conn.send(b"OK")
                            with open(song_path, "rb") as f:
                                while chunk := f.read(1024):
                                    conn.sendall(chunk)
                            print("[SERVER] Transfer complete")
                        else:
                            conn.send(b"ERROR: Invalid index")
                    except:
                        conn.send(b"ERROR: Failed to parse index")
                else:
                    conn.send(b"ERROR: Unknown command")
