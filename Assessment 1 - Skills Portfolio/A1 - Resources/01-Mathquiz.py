import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import pygame

# The following global functions have been established in this code section for a math quiz application:  
# In the meantime, EASY_BG_IMAGE, MODERATE_BG_IMAGE, and ADVANCED_BG_IMAGE specify the file paths to distinct background images
# ("Background1.png", "moderate.png", and "top-view-school-supplies-table-assortment.jpg")
# that are loaded and displayed behind the quiz interface to visually distinguish between Easy, Moderate, and Advanced modes, 
# improving the user experience and overall immersion. NUM_QUESTAINS sets the total number of questions per session to 10, guaranteeing a uniform quiz length across all difficulty levels.

NUM_QUESTIONS = 10
EASY_BG_IMAGE = "Background1.png"
ADVANCED_BG_IMAGE = "top-view-school-supplies-table-assortment.jpg"
MODERATE_BG_IMAGE = "moderate.png"