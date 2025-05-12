import os

class Admin:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Admin, cls).__new__(cls)
            cls._instance.users = []
            cls._instance.artists = []
            # Actualizează căile cu locația reală a fișierelor MP3
            songs_dir = os.path.join(os.path.dirname(__file__), "songs")
            cls._instance.songs = [
                
                os.path.join(songs_dir, "Godfather_HipHop.mp3"),
                os.path.join(songs_dir, "The New Orleans Tango.mp3"),
                os.path.join(songs_dir, "L'altra dimensione.mp3")
            ]
        return cls._instance
    
    def add_user(self, user):
        self.users.append(user)
    
    def add_artist(self, artist):
        self.artists.append(artist)
    
    def add_song(self, song_path):
        self.songs.append(song_path)