import socket
import pygame
import os

def request_song(index, host="192.168.1.100", port=12345):  # IP-ul serverului
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(f"request_song:{index}".encode())

        response = s.recv(2)
        if response != b"OK":
            print("[CLIENT] Error: Server did not accept the request.")
            return

        with open("temp_song.mp3", "wb") as f:
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                f.write(chunk)

        print("[CLIENT] Song received. Playing...")

        pygame.mixer.init()
        pygame.mixer.music.load("temp_song.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        print("[CLIENT] Done playing.")
        os.remove("temp_song.mp3")
