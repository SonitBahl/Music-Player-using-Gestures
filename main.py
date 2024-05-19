import os
import random
import pygame
import cv2
import mediapipe as mp
from tkinter import *
from tkinter import filedialog, messagebox
import threading
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("300x200")
        self.root.attributes("-topmost", True)

        pygame.mixer.init()

        self.music_folder = filedialog.askdirectory()
        self.playlist = []
        self.current_song_index = 0

        self.load_music()

        self.playing = False
        self.cooldown = False

        self.play_button = Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.next_button = Button(self.root, text="Next", command=self.next_music)
        self.next_button.pack(pady=10)

        self.prev_button = Button(self.root, text="Previous", command=self.prev_music)
        self.prev_button.pack(pady=10)

        self.action_label = Label(self.root, text="")
        self.action_label.pack(pady=10)

        self.setup_gesture_recognition()

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
            self.update_action_label("Play")
        else:
            pygame.mixer.music.stop()
            self.playing = False
            self.play_button.config(text="Play")
            self.update_action_label("Stop")

    def pause_music(self):
        if not self.playlist:
            return

        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.pause_button.config(text="Unpause")
            self.update_action_label("Pause")
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.pause_button.config(text="Pause")
            self.update_action_label("Unpause")

    def next_music(self):
        if not self.playlist:
            return

        self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_song_index])
        pygame.mixer.music.play()
        self.playing = True
        self.play_button.config(text="Stop")
        self.update_action_label("Next")

    def prev_music(self):
        if not self.playlist:
            return

        self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_song_index])
        pygame.mixer.music.play()
        self.playing = True
        self.play_button.config(text="Stop")
        self.update_action_label("Previous")

    def setup_gesture_recognition(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

        self.cap = cv2.VideoCapture(0)

        self.gesture_thread = threading.Thread(target=self.gesture_recognition)
        self.gesture_thread.daemon = True
        self.gesture_thread.start()

    def gesture_recognition(self):
        while True:
            success, image = self.cap.read()
            if not success:
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)  

            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]

                    if not self.cooldown:
                        if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y:
                            self.play_music()
                            self.set_cooldown()
                        elif index_tip.x < wrist.x:
                            self.prev_music()
                            self.set_cooldown()
                        elif index_tip.x > wrist.x:
                            self.next_music()
                            self.set_cooldown()

            cv2.imshow("Hand Gesture Recognition", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def set_cooldown(self):
        self.cooldown = True
        threading.Timer(2, self.reset_cooldown).start()

    def reset_cooldown(self):
        self.cooldown = False

    def update_action_label(self, action):
        self.action_label.config(text=f"Action: {action}")

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()
