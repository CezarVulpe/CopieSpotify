from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import scrolledtext
import pygame
from admin import Admin
import time

# Abstract User class
class UserAbstract(ABC):
    def __init__(self, username, age, city):
        self.username = username
        self.age = age
        self.city = city

    @abstractmethod
    def get_details(self):
        pass

# Abstract Content Creator class
class ContentCreator(UserAbstract):
    def __init__(self, username, age, city, description):
        super().__init__(username, age, city)
        self.description = description

    @abstractmethod
    def get_creator_info(self):
        pass

# User class
class User(UserAbstract):
    def __init__(self, username, age, city):
        super().__init__(username, age, city)

    def get_details(self):
        return f"User: {self.username}, Age: {self.age}, City: {self.city}"

# Artist class
class Artist(ContentCreator):
    def __init__(self, username, age, city, description):
        super().__init__(username, age, city, description)

    def get_details(self):
        return f"Artist: {self.username}, Age: {self.age}, City: {self.city}, Description: {self.description}"

    def get_creator_info(self):
        return f"Artist Bio: {self.description}"

# Function to open user window
def open_user_window(root, username):
    user_window = tk.Toplevel(root)
    user_window.title(f"User: {username}")
    user_window.geometry("800x550")
    user_window.configure(bg="#282c34")

    label = tk.Label(user_window, text=f"Welcome, {username}!", font=("Arial", 14), fg="white", bg="#282c34")
    label.pack(pady=10)

    entry = tk.Entry(user_window, width=60, font=("Arial", 12))
    entry.pack(pady=10)

    pygame.mixer.init()
    admin = Admin()

    text_area = scrolledtext.ScrolledText(user_window, width=80, height=15, font=("Arial", 10), bg="#1e222a", fg="white")
    text_area.pack(pady=10)

    player = None
    current_index = [-1]
    current_start_time = [0.0]  # timestamp when song started

    def get_current_position():
        millis = pygame.mixer.music.get_pos()
        if millis == -1:
            return 0.0
        return (millis / 1000.0) + current_start_time[0]

    def play_song(start_time=0.0):
        nonlocal player
        command = entry.get().strip().lower()
        if command.startswith("play song") or start_time > 0.0:
            try:
                if start_time == 0.0:
                    song_index = int(command.split(" ")[-1]) - 1
                else:
                    song_index = current_index[0]
                if 0 <= song_index < len(admin.songs):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(admin.songs[song_index])
                    pygame.mixer.music.play(start=start_time)
                    current_index[0] = song_index
                    current_start_time[0] = start_time
                    if start_time == 0.0:
                        text_area.insert(tk.END, f"Playing {admin.songs[song_index]}...\n")
                    else:
                        text_area.insert(tk.END, f"Resumed {admin.songs[song_index]} from {int(start_time)}s...\n")
                else:
                    text_area.insert(tk.END, "The requested song does not exist.\n")
            except ValueError:
                text_area.insert(tk.END, "Invalid command format. Use 'play song1', 'play song2', etc.\n")
        else:
            text_area.insert(tk.END, "Unknown command!\n")
        entry.delete(0, tk.END)

    def play_next_song():
        if not admin.songs:
            text_area.insert(tk.END, "No songs available.\n")
            return
        next_index = (current_index[0] + 1) % len(admin.songs)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(admin.songs[next_index])
        pygame.mixer.music.play()
        current_index[0] = next_index
        current_start_time[0] = 0.0
        text_area.insert(tk.END, f"Playing next: {admin.songs[next_index]}\n")

    def play_previous_song():
        if not admin.songs:
            text_area.insert(tk.END, "No songs available.\n")
            return
        previous_index = (current_index[0] - 1 + len(admin.songs)) % len(admin.songs)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(admin.songs[previous_index])
        pygame.mixer.music.play()
        current_index[0] = previous_index
        current_start_time[0] = 0.0
        text_area.insert(tk.END, f"Playing previous: {admin.songs[previous_index]}\n")

    def skip_forward():
        pos = get_current_position()
        new_start = pos + 5.0
        pygame.mixer.music.stop()
        pygame.mixer.music.load(admin.songs[current_index[0]])
        pygame.mixer.music.play(start=new_start)
        current_start_time[0] = new_start
        text_area.insert(tk.END, "Skipped forward 5 seconds.\n")

    def skip_backward():
        pos = get_current_position()
        new_start = max(0.0, pos - 5.0)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(admin.songs[current_index[0]])
        pygame.mixer.music.play(start=new_start)
        current_start_time[0] = new_start
        if new_start == 0.0:
            text_area.insert(tk.END, "Restarted song.\n")
        else:
            text_area.insert(tk.END, "Skipped backward 5 seconds.\n")

    def stop_song():
        pygame.mixer.music.stop()
        text_area.insert(tk.END, "Music stopped.\n")

    button_frame = tk.Frame(user_window, bg="#282c34")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Play Song", font=("Arial", 12), command=play_song, bg="#61afef", fg="black").grid(row=0, column=0, padx=10, pady=5)
    tk.Button(button_frame, text="Play Next Song", font=("Arial", 12), command=play_next_song, bg="#98c379", fg="black").grid(row=0, column=1, padx=10, pady=5)
    tk.Button(button_frame, text="Play Previous Song", font=("Arial", 12), command=play_previous_song, bg="#c678dd", fg="black").grid(row=0, column=2, padx=10, pady=5)
    tk.Button(button_frame, text="Skip +5s", font=("Arial", 12), command=skip_forward, bg="#d19a66", fg="black").grid(row=0, column=3, padx=10, pady=5)
    tk.Button(button_frame, text="Skip -5s", font=("Arial", 12), command=skip_backward, bg="#56b6c2", fg="black").grid(row=0, column=4, padx=10, pady=5)
    tk.Button(button_frame, text="Stop Music", font=("Arial", 12), command=stop_song, bg="#e06c75", fg="black").grid(row=0, column=5, padx=10, pady=5)
