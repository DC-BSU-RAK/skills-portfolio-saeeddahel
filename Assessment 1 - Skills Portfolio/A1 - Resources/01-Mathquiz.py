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


def displayMenu(root, start_callback, bg_images):
    """Display stylized image as main menu with clickable zones."""
    canvas = tk.Canvas(root, width=800, height=500, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    
    menu_img = Image.open("Background2.png").resize((800, 500), Image.Resampling.LANCZOS)
    menu_img_tk = ImageTk.PhotoImage(menu_img)
    canvas.create_image(0, 0, anchor="nw", image=menu_img_tk)
    canvas.image = menu_img_tk  

    # This section uses a full-screen background image on a Tkinter Canvas to generate and show the main menu.  
    # The canvas has fixed dimensions (800x500) and is centred in the root window.  
    # PIL is used to load the "Background2.png" image, which is then resized to fit the canvas using high-quality LANCZOS resampling and transformed into a Tkinter-compatible PhotoImage.  
    # After that, it is drawn at the canvas' upper-left corner (anchor="nw"). 
    # To keep Python's garbage collector from erasing the image too soon and guarantee that it stays visible for the duration of the menu, the reference `canvas.image = menu_img_tk` is important.

    regions = {
        "Easy": (270, 200, 530, 250),
        "Moderate": (270, 300, 530, 350),
        "Advanced": (270, 380, 530, 430),
    }

    # Each difficulty level ("Easy", "Moderate", and "Advanced") is mapped to a tuple of coordinates (x1, y1, x2, y2) in pixels by this dictionary, 
    # which also defines the clickable rectangular regions on the main menu canvas. 
    # The top-left (x1, y1) and bottom-right (x2, y2) corners of invisible hitboxes superimposed on the menu image are represented by these coordinates.  
    # The corresponding difficulty is identified and sent to the quiz startup logic when the user clicks inside one of these zones. 
    # The regions in "Background2.png" are arranged with precision to match the text or visual buttons, 
    # allowing for simple point-and-click navigation without the need for conventional GUI buttons.

    def on_click(event):
        for level, (x1, y1, x2, y2) in regions.items():
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                canvas.destroy()
                start_callback(level, bg_images)

    canvas.bind("<Button-1>", on_click)


def randomInt(difficulty):
    if difficulty == "Easy":
        return 0, 9
    elif difficulty == "Moderate":
        return 10, 99
    elif difficulty == "Advanced":
        return 1000, 9999
    return 0, 9


def decideOperation():
    return random.choice(["+", "-"])


def isCorrect(user_answer_str, correct_answer):
    try:
        user_answer = int(user_answer_str.strip())
    except:
        return False
    return user_answer == correct_answer


def displayResults(root, score):
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"
    msg = f"Your score: {score}/100\nGrade: {grade}\n\nPlay again?"
    return messagebox.askyesno("Quiz Results", msg)


class MathsQuizApp:
    def __init__(self, root, bg_images, correct_sound, wrong_sound):
        self.root = root
        self.bg_images = bg_images
        self.correct_sound = correct_sound
        self.wrong_sound = wrong_sound

        self.background_label = tk.Label(root, image=bg_images["Easy"], borderwidth=0)
        self.background_label.place(relwidth=1, relheight=1)

        
        displayMenu(root, self.start_quiz, bg_images)

    def start_quiz(self, difficulty, bg_images):

        # To begin a new quiz, this line of code first clears all widgets except the background and then resets important variables,
        # including the difficulty, score, and question index, as well as the attempt counter.

        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()

        self.difficulty = difficulty
        self.current_q = 0
        self.raw_score = 0
        self.attempt = 1

        # Depending on the selected difficulty, this section of the code changes the quiz interface.  
        # It creates the main quiz layout, which includes the question, answer input, feedback, and navigation elements, modifies the background image, and specifies font styles and colours.
        # In order to guarantee that the quiz's flow and graphics adapt fluidly to each degree of difficulty, 
        # it also sets up interactive bindings for answering questions and going back to the main menu.

        bg_key = {"Advanced": "Advanced", "Moderate": "Moderate"}.get(difficulty, "Easy")
        self.background_label.config(image=bg_images[bg_key])
        self.background_label.image = bg_images[bg_key]

        quiz_font_large = ("VT323", 26)
        quiz_font_med = ("VT323", 20)
        quiz_font_small = ("VT323", 16)

        bg_color = "#4C00FF"
        entry_bg = "#3A0CA3"

        self.quiz_frame = tk.Frame(self.root, bg=bg_color, highlightthickness=0, bd=0)
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.header_label = tk.Label(
            self.quiz_frame,
            text="",
            font=quiz_font_large,
            fg="white",
            bg=bg_color,
        )
        self.header_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.question_label = tk.Label(
            self.quiz_frame,
            text="",
            font=quiz_font_med,
            fg="white",
            bg=bg_color,
        )
        self.question_label.grid(row=1, column=0, columnspan=3, pady=(0, 14))

        tk.Label(
            self.quiz_frame,
            text="Your answer:",
            font=quiz_font_small,
            fg="white",
            bg=bg_color,
        ).grid(row=2, column=0, sticky="e")

        self.answer_entry = tk.Entry(
            self.quiz_frame,
            width=8,
            font=quiz_font_small,
            fg="white",
            bg=entry_bg,
            insertbackground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.answer_entry.grid(row=2, column=1)
        self.answer_entry.bind("<Return>", lambda e: self.submit_answer())

        tk.Button(
            self.quiz_frame,
            text="Submit",
            font=quiz_font_small,
            fg="white",
            bg="#560BAD",
            activebackground="#7209B7",
            activeforeground="white",
            relief="flat",
            command=self.submit_answer,
        ).grid(row=2, column=2, padx=(10, 0))

        self.feedback_label = tk.Label(
            self.quiz_frame,
            text="",
            font=quiz_font_small,
            fg="white",
            bg=bg_color,
        )
        self.feedback_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        tk.Button(
            self.quiz_frame,
            text="Back to Menu",
            font=quiz_font_small,
            fg="white",
            bg="#3F37C9",
            activebackground="#4895EF",
            activeforeground="white",
            relief="flat",
            command=self.return_to_menu,
        ).grid(row=4, column=0, columnspan=3, pady=(25, 0))

        self.next_problem()

    def next_problem(self):
        if self.current_q >= NUM_QUESTIONS:
            percent = round((self.raw_score / (NUM_QUESTIONS * 10)) * 100)
            self.quiz_frame.destroy()
            play_again = displayResults(self.root, percent)
            if play_again:
                displayMenu(self.root, self.start_quiz, self.bg_images)
            else:
                self.root.quit()
            return

        self.attempt = 1
        self.current_q += 1

        minv, maxv = randomInt(self.difficulty)
        a = random.randint(minv, maxv)
        b = random.randint(minv, maxv)
        op = decideOperation()
        if op == "-" and a < b:
            a, b = b, a
        self.num1, self.num2, self.op = a, b, op
        self.correct_answer = a + b if op == "+" else a - b

        self.header_label.config(text=f"Difficulty: {self.difficulty} — Question {self.current_q}/{NUM_QUESTIONS}")
        self.question_label.config(text=f"{a} {op} {b} =")
        self.feedback_label.config(text="Attempt 1: worth 10 points")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()

    def submit_answer(self):
        user_text = self.answer_entry.get().strip()
        if not user_text:
            self.feedback_label.config(text="Please enter an answer.")
            return

        correct = isCorrect(user_text, self.correct_answer)

        if correct:
            if self.correct_sound:
                self.correct_sound.play()
            gained = 10 if self.attempt == 1 else 5
            self.raw_score += gained
            self.feedback_label.config(text=f"Correct! +{gained} points.")
            self.root.after(700, self.next_problem)
        else:
            if self.wrong_sound:
                self.wrong_sound.play()
            if self.attempt == 1:
                self.attempt = 2
                self.feedback_label.config(text="Incorrect. Try again — worth 5 points.")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()
            else:
                self.feedback_label.config(text=f"Incorrect. The correct answer was {self.correct_answer}.")
                self.root.after(1000, self.next_problem)

    def return_to_menu(self):
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()
        self.background_label.config(image=self.bg_images["Easy"])
        self.background_label.image = self.bg_images["Easy"]
        displayMenu(self.root, self.start_quiz, self.bg_images)


def run_app():
    root = tk.Tk()
    root.title("Maths Quiz")
    root.geometry("800x500")
    root.resizable(False, False)