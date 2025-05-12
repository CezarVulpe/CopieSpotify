import pygame
import os

def play_music():
    pygame.mixer.init()
    song_path = os.path.join(os.path.dirname(__file__), "songs", "Godfather_HipHop.mp3")
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        print("Redarea a început! Verifică dacă se aude sunetul.")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    play_music()