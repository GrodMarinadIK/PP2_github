import os
import pygame
import random

class MusicPlayer:
    """
    Handles music playback logic, playlist management, and volume control.
    """
    
    def __init__(self):
        pygame.mixer.init()
        # Resolve path to the 'music' directory relative to this script
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(base_path, "music")
        
        # Scan directory for MP3 files
        self.playlist = [f for f in os.listdir(self.music_dir) if f.endswith('.mp3')]
        self.current_track_index = 0
        
        # Initial volume setting
        self.volume = 0.1
        pygame.mixer.music.set_volume(self.volume)
        self.is_paused = False
        
    def shuffle_playlist(self):
        """
        Shuffles the playlist while ensuring the new first track isn't 
        the one that was just playing.
        """
        if len(self.playlist) > 1:
            current_song = self.playlist[self.current_track_index]
            random.shuffle(self.playlist)
            # Prevent instant replay of the same song after shuffle
            if self.playlist[0] == current_song:
                self.playlist.append(self.playlist.pop(0))        
            self.current_track_index = 0
            self.play()        
            
    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.1)
        pygame.mixer.music.set_volume(self.volume)
        
    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def get_current_track_path(self):
        """Returns the full OS-compatible path for the currently selected track."""
        return os.path.join(self.music_dir, self.playlist[self.current_track_index])

    def play(self):
        if self.playlist:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            elif not pygame.mixer.music.get_busy():
                track_path = self.get_current_track_path()
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()

    def stop(self):
        if self.playlist:
            pygame.mixer.music.pause()
            self.is_paused = True

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        pygame.mixer.music.stop() # Останавливаем старый трек
        self.is_paused = False    # Сбрасываем паузу, если она была
        self.play()               # Теперь play() увидит, что ничего не занято, и загрузит новый трек

    def prev_track(self):
        """Switches to the previous track with circular indexing."""
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play()