import tkinter as tk
from PIL import Image, ImageTk
import random
import win32com.client
import threading
import pygame


# The jokes are loaded from a text file and returned as a list of (setup, punchline) pairs by this function. 
# Each line is read, the setup and punchline are separated at the first question mark, and the lines are then stored as tuples. 
# A default error message claiming that the jokes file could not be located is returned if the file is missing.

def load_jokes(filename="randomJokes.txt"):
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
