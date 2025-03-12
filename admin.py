# main.py (Admin-related logic)
class Admin:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Admin, cls).__new__(cls)
            cls._instance.users = []
            cls._instance.artists = []
            cls._instance.songs = [
                "If The Godfather Was Hip Hop- feat. Simply Three (violin, cello, bass).mp3",
                "The New Orleans Tango (2024) - Tony DeSare.mp3"
            ]
        return cls._instance
    
    def add_user(self, user):
        self.users.append(user)
    
    def add_artist(self, artist):
        self.artists.append(artist)
    
    def add_song(self, song):
        self.songs.append(song)