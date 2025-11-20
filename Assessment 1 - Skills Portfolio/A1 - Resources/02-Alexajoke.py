import tkinter as tk
from PIL import Image, ImageTk
import random
import win32com.client
import threading
import pygame
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")
bg_path = os.path.join(assets_dir, "joke.png")






# The jokes are loaded from a text file and returned as a list of (setup, punchline) pairs by this function. 
# Each line is read, the setup and punchline are separated at the first question mark, and the lines are then stored as tuples. 
# A default error message claiming that the jokes file could not be located is returned if the file is missing.

def load_jokes(filename=os.path.join(assets_dir, "randomJokes.txt")):
    jokes = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if "?" in line:
                    setup, punchline = line.strip().split("?", 1)
                    jokes.append((setup + "?", punchline))
    except FileNotFoundError:
        jokes = [("Error:", "randomJokes.txt not found.")]
    return jokes

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Machine")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        # Text-to-speech functionality is enabled by initialising the SAPI voice engine in this portion of the code. 
        # When the program begins, it plays a welcome message, creates a speech object, and adjusts the speaking rate and volume. 
        # It detects the error and prints a message pointing to the problem if the setup fails.

        try:
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            self.speaker.Rate = 1
            self.speaker.Volume = 100
            self.speaker.Speak("Welcome to saeeds joke machine", 1)  
            print("SAPI voice initialized")
        except Exception as e:
            print(f"SAPI init failed: {e}")
             # In order for Pygame to play sound effects, this section of code initialises the audio mixer.
         # We generate a list of the available laugh tracks # (laugh.mp3, laugh2.mp3, and Funny.mp3) if the mixer loads successfully. 
         #  One of these files will be chosen at random by the program and played through the mixer when a punchline is displayed later. 
         # An exception is caught and an error message is printed rather than the program crashing if the mixer does not initialise, 
         # which is typically caused by missing audio hardware or a device conflict.

        try:
            pygame.mixer.init()
            self.laugh_sounds = [
    os.path.join(assets_dir, "laugh.mp3"),
    os.path.join(assets_dir, "laugh2.mp3"),
    os.path.join(assets_dir, "Funny.mp3")
]

  
            print("pygame mixer initialized")
        except Exception as e:
            print(f"pygame mixer init failed: {e}")


        # This section creates the joke machine's main interface, which includes the title banner, background canvas, and central card that shows the punchline and joke setup. 
        # In addition to filling the window, the large canvas serves as an interactive space with invisible rectangular regions that serve as buttons for delivering jokes, 
        # revealing punchlines, switching to the next joke, or ending the program. 
        # A fade-in text effect is used to dynamically update the labels inside the styled card frame, and click detection on the canvas initiates the relevant functions for sound playback,
        # speech output, and joke display.  
        # The user can only reveal the punchline or advance when permitted because the flags "can_show_punchline" and "can_next" regulate the flow.

        self.canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        bg_image = Image.open(bg_path).resize((1280, 720))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.jokes = load_jokes()
        self.current_joke = None

        self.canvas.create_text(
            640, 50, text=" 🤡Alexa, Tell Me a Joke!🤡",
            font=("Arial", 28, "bold"), fill="#080808", tags="banner"
        )

        self.card_frame = tk.Frame(root, bg="#1A202C")
        self.card_frame.place(x=640, y=300, anchor="center", width=700, height=280)
        self.card_frame.config(highlightbackground="#FFD700", highlightthickness=2)

        self.setup_label = tk.Label(
            self.card_frame, text="", font=("Arial", 18),
            wraplength=650, fg="#FFFFFF", bg="#1A202C", justify="center"
        )
        self.setup_label.pack(pady=20)

        self.punchline_label = tk.Label(
            self.card_frame, text="", font=("Arial", 18, "italic"),
            fg="#90CDF4", bg="#1A202C", wraplength=650, justify="center"
        )
        self.punchline_label.pack(pady=10)

        self.regions = {
            "Tell Joke": (50, 470, 380, 530),
            "Show Punchline": (50, 540, 380, 610),
            "Next Joke": (50, 630, 380, 680),
            "Exit": (400, 660, 1280, 710)
        }

        self.canvas.bind("<Button-1>", self.on_click)

        self.can_show_punchline = False
        self.can_next = False

    def speak_text(self, text):
        def run():
            try:
                print(f"[SPEAK] {text}")
                self.speaker.Speak(text, 1)
            except Exception as e:
                print(f"[SPEAK ERROR] {e}")
        threading.Thread(target=run, daemon=True).start()

    def show_joke(self, event=None):
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text="")
        self.punchline_label.config(text="")
        self.fade_in_label(self.setup_label, self.current_joke[0])
        self.speak_text(self.current_joke[0])
        self.can_show_punchline = True
        self.can_next = False


    def show_punchline(self, event=None):
        if self.current_joke and self.can_show_punchline:
           self.fade_in_label(self.punchline_label, self.current_joke[1])
           self.speak_text(self.current_joke[1])
           self.play_joke_sound()  
           self.can_show_punchline = False
           self.can_next = True


    def fade_in_label(self, label, full_text, index=0):
        if index <= len(full_text):
            label.config(text=full_text[:index])
            self.root.after(20, lambda: self.fade_in_label(label, full_text, index + 1))

    def on_click(self, event):
        print(f"Clicked at: {event.x}, {event.y}")
        for action, (x1, y1, x2, y2) in self.regions.items():
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if action == "Tell Joke":
                    self.show_joke()
                elif action == "Show Punchline":
                    self.show_punchline()
                elif action == "Next Joke":
                    self.show_joke()
                elif action == "Exit":
                    self.root.quit()
                break
    def play_joke_sound(self):
        def run():
            try:
               sound = random.choice(self.laugh_sounds)
               print(f"[AUDIO] Playing: {sound}")
               pygame.mixer.music.load(sound)
               pygame.mixer.music.play()
            except Exception as e:
                print(f"[AUDIO ERROR] {e}")
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
