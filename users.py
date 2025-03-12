# users.py
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import scrolledtext
import pygame
from admin import Admin

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
# Function to open user window
# Function to open user window
def open_user_window(root, username):
    user_window = tk.Toplevel(root)
    user_window.title(f"User: {username}")
    user_window.geometry("500x400")
    user_window.configure(bg="#282c34")
    
    label = tk.Label(user_window, text=f"Welcome, {username}!", font=("Arial", 14), fg="white", bg="#282c34")
    label.pack(pady=10)
    
    entry = tk.Entry(user_window, width=40, font=("Arial", 12))
    entry.pack(pady=10)
    
    pygame.mixer.init()
    admin = Admin()
    
    text_area = scrolledtext.ScrolledText(user_window, width=50, height=10, font=("Arial", 10), bg="#1e222a", fg="white")
    text_area.pack(pady=10)
    
    def play_song():
        command = entry.get().strip().lower()
        if command.startswith("play song"):
            try:
                song_index = int(command.split(" ")[-1]) - 1
                if 0 <= song_index < len(admin.songs):
                    player = pygame.mixer.Sound(admin.songs[song_index])
                    player.play()
                    text_area.insert(tk.END, f"Playing {admin.songs[song_index]}...\n")
                else:
                    text_area.insert(tk.END, "The requested song does not exist.\n")
            except ValueError:
                text_area.insert(tk.END, "Invalid command format. Use 'play song1', 'play song2', etc.\n")
        else:
            text_area.insert(tk.END, "Unknown command!\n")
        entry.delete(0, tk.END)
    
    def stop_song():
        pygame.mixer.stop()
        text_area.insert(tk.END, "Music stopped.\n")
    
    play_button = tk.Button(user_window, text="Play Song", font=("Arial", 12), command=play_song, bg="#61afef", fg="black")
    play_button.pack(pady=5)
    
    stop_button = tk.Button(user_window, text="Stop Music", font=("Arial", 12), command=stop_song, bg="#e06c75", fg="black")
    stop_button.pack(pady=5)