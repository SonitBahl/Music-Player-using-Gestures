import os
import random
import pygame
from tkinter import *
from tkinter import filedialog, messagebox

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Music Player")
        self.root.geometry("300x200")

        pygame.mixer.init()

        self.music_folder = filedialog.askdirectory()
        self.playlist = []
        self.current_song_index = 0

        self.load_music()

        self.playing = False

        self.play_button = Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.next_button = Button(self.root, text="Next", command=self.next_music)
        self.next_button.pack(pady=10)

        self.prev_button = Button(self.root, text="Previous", command=self.prev_music)
        self.prev_button.pack(pady=10)

    def load_music(self):
        if not self.music_folder:
            messagebox.showerror("Error", "No folder selected!")
            return

        for file in os.listdir(self.music_folder):
            if file.endswith(".mp3"):
                self.playlist.append(os.path.join(self.music_folder, file))

        if not self.playlist:
            messagebox.showerror("Error", "No mp3 files found in the folder!")
            return

        random.shuffle(self.playlist)

    def play_music(self):
        if not self.playlist:
            return

        if not self.playing:
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play()
            self.playing = True
            self.play_button.config(text="Stop")
        else:
            pygame.mixer.music.stop()
            self.playing = False
            self.play_button.config(text="Play")

    def pause_music(self):
        if not self.playlist:
            return

        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.pause_button.config(text="Unpause")
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.pause_button.config(text="Pause")

    def next_music(self):
        if not self.playlist:
            return

        self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_song_index])
        pygame.mixer.music.play()
        self.playing = True
        self.play_button.config(text="Stop")

    def prev_music(self):
        if not self.playlist:
            return

        self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_song_index])
        pygame.mixer.music.play()
        self.playing = True
        self.play_button.config(text="Stop")

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()
