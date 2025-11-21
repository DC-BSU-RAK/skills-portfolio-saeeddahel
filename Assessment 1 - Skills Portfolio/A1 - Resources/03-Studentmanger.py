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