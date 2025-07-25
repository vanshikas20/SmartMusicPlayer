# music controller
from db_playlist import get_songs, insert_play_history, get_song_id
import pygame

# Initialize sound mixer
pygame.mixer.init()

# Fetch songs from the database
songs = get_songs()  # This will return a list of tuples (song_name, song_path)
current_index = 0
is_playing = False
is_paused = False

def load_playlist():
    """Initialize the playlist from database"""
    global songs, current_index
    songs = get_songs()
    current_index = 0 if songs else -1
    print(f"🎵 Loaded {len(songs)} songs from database")

def setPlaylist(new_playlist):
    global songs
    songs = new_playlist

def get_current_song_path():
    """Returns the current song path or None"""
    if songs and 0 <= current_index < len(songs):
        return songs[current_index][1]  # Return the path part of the tuple
    return None

def playMusic():
    global is_playing, is_paused
    if is_paused: #checks if song is paused
        return resumeMusic()

    song_path = get_current_song_path()
    if not song_path:
        print("⚠️ No song selected!")
        return

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play() #plays the music
        is_playing = True
        is_paused = False

        if song_id := get_song_id(song_path): #insert it in history table
            insert_play_history(song_id)

    except Exception as e:
        print(f"Error: {e}")

def pause():
    global is_paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True
    else:
        pygame.mixer.music.unpause()
        is_paused = False

def resumeMusic():
    global is_paused #resume the music
    pygame.mixer.music.unpause()
    is_paused = False

def play_next():
    global current_index, is_playing, is_paused
    if current_index < len(songs) - 1:
        current_index += 1
        playMusic()
    else:
        print("Already at last song 🎵")

def play_previous():
    global current_index, is_playing, is_paused
    if current_index > 0:
        current_index -= 1
        playMusic()
    else:
        print("Already at first song 🎵")