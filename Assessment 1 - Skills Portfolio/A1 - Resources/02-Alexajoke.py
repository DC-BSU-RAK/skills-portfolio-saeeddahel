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
