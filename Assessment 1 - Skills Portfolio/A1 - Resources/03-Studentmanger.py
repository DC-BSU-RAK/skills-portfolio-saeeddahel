import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk


DATA_PATHS = ["/mnt/data/studentMarks.txt", "studentMarks.txt"]
BG_IMAGE_PATHS = ["/mnt/data/s2.png", "s2.png"]
POTENTIAL_MAX = 160.0


# The Student class encapsulates a student's academic record by storing their ID, name, three coursework marks, and exam mark, 
# while providing computed properties for total coursework, overall score, percentage, and letter grade based on a 160-point maximum.
# It ensures data integrity through type conversion and stripping of whitespace, offers a clean formatted() method for human-readable output,
# and includes a to_line() method to serialize the record back into the exact CSV format expected by the studentMarks.txt file—enabling seamless persistence 
# and interoperability with the rest of the system.

class Student:
    def __init__(self, sid, name, c1, c2, c3, exam):
        self.sid = str(sid).strip()
        self.name = name.strip()
        self.coursework = [int(c1), int(c2), int(c3)]
        self.exam = int(exam)

    @property
    def coursework_total(self): return sum(self.coursework)
    @property
    def total(self): return self.coursework_total + self.exam
    @property
    def percentage(self): return (self.total / POTENTIAL_MAX) * 100

    @property
    def grade(self):
        p = self.percentage
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"

    def formatted(self):
        return (
            f"Name: {self.name}\n"
            f"Student ID: {self.sid}\n"
            f"Coursework marks: {self.coursework} (Total: {self.coursework_total})\n"
            f"Exam mark: {self.exam}\n"
            f"Overall total: {self.total}/160\n"
            f"Percentage: {self.percentage:.2f}%\n"
            f"Grade: {self.grade}\n"
        )

    def to_line(self):
        """CSV line exactly as the original file expects"""
        return f"{self.sid},{self.name},{self.coursework[0]},{self.coursework[1]},{self.coursework[2]},{self.exam}\n"

# The _get_data_path() helper function allows the program to operate both locally and in isolated environments (e.g., /mnt/data) 
# by searching a predefined list of potential file locations (DATA_PATHS) and returning the first path to studentMarks.txt that exists. 
# To prepare the data for use in the application, the load_students() function opens and reads the student data file in UTF-8 encoding using this path.
# It then safely loads each non-empty line into memory after filtering out empty lines.
# To avoid crashes and guarantee stable startup behaviour, it returns an empty list and shows a user-friendly error via a message box if the file cannot be located.


def _get_data_path():
    return next((p for p in DATA_PATHS if os.path.exists(p)), None)

def load_students():
    path = _get_data_path()
    if not path:
        messagebox.showerror("File not found", "studentMarks.txt not found.")
        return []

    students = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    try:
        int(lines[0])
        lines = lines[1:]
    except ValueError:
        pass

    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 6:
            sid, name, c1, c2, c3, exam = parts
            students.append(Student(sid, name, c1, c2, c3, exam))
    return students


def save_students(students):
    """Overwrite the file with the current list (preserve optional count line)"""
    path = _get_data_path()
    if not path:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{len(students)}\n")               
        for s in students:
            f.write(s.to_line())
    return True


# The main GUI window is created using Tkinter by the StudentManagerApp class, 
# which disables resizing to preserve a consistent chalkboard-style layout and sets a fixed 1920x1080 resolution with a unique title.  
# To ensure that all following operations—viewing, sorting, adding, or editing records—work with the most recent in-memory data from the beginning, 
# the __init__ method loads student data from studentMarks.txt immediately using the load_students() function and stores it in self.students.  
# This configuration lays the groundwork for a desktop application that is responsive, data-driven, and has a polished layout with a classroom theme.

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Saeed-Dahel-Student-Manager-System")
        self.root.geometry("1920x1080")
        self.root.resizable(False, False)
        self.students = load_students()

        # This code creates a static, chalkboard-themed visual foundation for the GUI by loading a background image and displaying it on a full-screen canvas.

        self.bg_image = self.load_bg_image()
        self.canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # To display results with a typewriter animation, a styled Text widget is made to resemble a chalkboard output area and is centred on the canvas at (960, 250).

        self.output_box = tk.Text(
            root,
            width=80,
            height=12,
            font=("Courier New", 18, "bold"),
            bg="#1e2e1c",
            fg="#e8e4d9",
            relief="flat",
            wrap="word",
            padx=40,
            pady=30,
            spacing1=6,
            spacing3=6,
            insertbackground="#e8e4d9"
        )
        self.canvas.create_window(960, 250, window=self.output_box, anchor="center")

        # In order to replicate realistic chalk writing, a typewriter-style animation function is defined and bound to the instance. 
        # It inserts text into the disabled output box character by character with various time delays for punctuation.

        def typewrite_text(self, full_text, delay=38):
            self.output_box.config(state="normal")
            self.output_box.delete("1.0", tk.END)
            self.output_box.config(state="disabled")

            self.current_text = full_text
            self.char_index = 0

            def write_next():
                if self.char_index < len(self.current_text):
                    char = self.current_text[self.char_index]
                    self.output_box.config(state="normal")
                    self.output_box.insert(tk.END, char)
                    self.output_box.see(tk.END)
                    self.output_box.config(state="disabled")
                    self.char_index += 1
                    extra = 25 if char in ".\n,!?" else 0
                    self.root.after(delay + extra, write_next)

            write_next()

        self.typewrite_text = typewrite_text.__get__(self)