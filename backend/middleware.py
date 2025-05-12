from flask import Flask, request, jsonify
from flask_cors import CORS
import pygame
import os
from admin import Admin

app = Flask(__name__)
CORS(app)

# Clasă pentru gestionarea player-ului
class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.admin = Admin()
        self.current_song_index = -1
        self.is_playing = False

    def play_song(self, song_index):
        if 0 <= song_index < len(self.admin.songs):
            try:
                pygame.mixer.music.load(self.admin.songs[song_index])
                pygame.mixer.music.play()
                self.current_song_index = song_index
                self.is_playing = True
                return True
            except Exception as e:
                print(f"Eroare la redare: {e}")
                return False
        return False
    
    def get_current_position(self):
        return pygame.mixer.music.get_pos() / 1000  # Convertim în secunde

    def get_song_duration(self, song_index):
        if 0 <= song_index < len(self.admin.songs):
            sound = pygame.mixer.Sound(self.admin.songs[song_index])
            return sound.get_length()
        return 0

player = MusicPlayer()

@app.route("/play", methods=["POST"])
def handle_play():
    data = request.get_json()
    song_index = data.get("song_index", 0)
    
    if player.play_song(song_index):
        song_name = os.path.basename(player.admin.songs[song_index])
        return jsonify({
            "status": "success",
            "message": f"Playing: {song_name}"
        })
    else:
        return jsonify({"status": "error", "message": "Invalid song index"}), 400

@app.route("/pause", methods=["POST"])
def handle_pause():
    if player.is_playing:
        pygame.mixer.music.pause()
        player.is_playing = False
        return jsonify({"status": "success", "message": "Paused"})
    return jsonify({"status": "error", "message": "No song playing"}), 400

@app.route("/get_songs", methods=["GET"])
def get_songs():
    songs = [os.path.basename(song) for song in player.admin.songs]
    return jsonify({"songs": songs})
@app.route("/get_current_song_info", methods=["GET"])

def get_current_info():
    duration = player.get_song_duration(player.current_song_index)
    current_pos = player.get_current_position()
    return jsonify({
        "duration": duration,
        "current_position": current_pos,
        "is_playing": player.is_playing
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)