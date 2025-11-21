import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATHS = [    os.path.join(BASE_DIR, "studentMarks.txt"),    "studentMarks.txt"]
BG_IMAGE_PATHS = [    os.path.join(os.path.dirname(__file__), "s2.png"),    "/mnt/data/s2.png",    "s2.png"]
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

        # When the app launches, a multiline welcome message with a list of all eight menu options is defined and scheduled to appear with a typewriter animation after 700 ms.

        welcome = (
            "       WELCOME TO THE STUDENT MANAGER PORTAL!       \n\n"
            "Please select an option below:\n\n"
            "  1. View All Records\n"
            "  2. View Individual Student\n"
            "  3. Highest Mark        \n"
            "  4. Lowest Mark         \n"
            "  5. Sort Records        \n"
            "  6. Add Record          \n"
            "  7. Delete Record       \n"
            "  8. Update Record       \n\n"
        )
        self.root.after(700, lambda: self.typewrite_text(welcome))

        # TITLE 

        self.canvas.create_text(964, 124, text="STUDENT MANAGER", fill="#2d4a2d",
                                font=("Comic Sans MS", 48, "bold"), anchor="center")
        self.canvas.create_text(960, 120, text="STUDENT MANAGER", fill="#f7f3e9",
                                font=("Comic Sans MS", 48, "bold"), anchor="center")

        # BUTTON STYLE 

        btn_style = {
            "font": ("Comic Sans MS", 15, "bold"),
            "width": 26,
            "height": 2,
            "bg": "#2c3e2c",
            "fg": "#e8e4d9",
            "activebackground": "#446644",
            "activeforeground": "white",
            "relief": "flat",
            "cursor": "hand2"
        }

        # BUTTONS (8 total) 

        self.btn1 = tk.Button(root, text="1. View All Records",    command=self.view_all,       **btn_style)
        self.btn2 = tk.Button(root, text="2. View Individual",     command=self.view_individual,**btn_style)
        self.btn3 = tk.Button(root, text="3. Highest Mark",        command=self.show_highest,   **btn_style)
        self.btn4 = tk.Button(root, text="4. Lowest Mark",         command=self.show_lowest,    **btn_style)
        self.btn5 = tk.Button(root, text="5. Sort Records",        command=self.sort_records,   **btn_style)
        self.btn6 = tk.Button(root, text="6. Add Record",          command=self.add_record,     **btn_style)
        self.btn7 = tk.Button(root, text="7. Delete Record",       command=self.delete_record,  **btn_style)
        self.btn8 = tk.Button(root, text="8. Update Record",       command=self.update_record,  **btn_style)

        # A neat, symmetrical menu layout is produced by placing eight buttons in a two-column grid on the canvas with balanced horizontal spacing (700, 1260) and vertical gaps of 100 pixels.

        left_x, right_x = 700, 1260
        top_y = 560
        gap_y = 100

        self.canvas.create_window(left_x,  top_y,           window=self.btn1, anchor="center")
        self.canvas.create_window(right_x, top_y,           window=self.btn2, anchor="center")
        self.canvas.create_window(left_x,  top_y + gap_y,   window=self.btn3, anchor="center")
        self.canvas.create_window(right_x, top_y + gap_y,   window=self.btn4, anchor="center")
        self.canvas.create_window(left_x,  top_y + 2*gap_y, window=self.btn5, anchor="center")
        self.canvas.create_window(right_x, top_y + 2*gap_y, window=self.btn6, anchor="center")
        self.canvas.create_window(left_x,  top_y + 3*gap_y, window=self.btn7, anchor="center")
        self.canvas.create_window(right_x, top_y + 3*gap_y, window=self.btn8, anchor="center")

        # With backup error handling in case pygame is not present or the file cannot be located,
        # this part of the code aims to initialise pygame, find, and play a background music file (work.mp3) on an infinite loop at low volume (0.23).

        try:
           import pygame, os

           pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

           BASE_DIR = os.path.dirname(os.path.abspath(__file__))
           music_path = os.path.join(BASE_DIR, "work.mp3")   

           if os.path.exists(music_path):
              pygame.mixer.music.load(music_path)
              pygame.mixer.music.play(-1)
              pygame.mixer.music.set_volume(0.23)
           else:
              print("work.mp3 not found:", music_path)

        except Exception as e:
            print("Music error:", e)


    # While _find_student searches for a student by ID or partial name match case-insensitively and returns the matching Student object or None, 
    # the load_bg_image method finds and loads the background image (s2.png) from possible paths, resizes it to fit the 1920×1080 window,
    # and returns a PhotoImage for the canvas—or displays an error and exits the application if it cannot be found. 

    def load_bg_image(self):
        path = next((p for p in BG_IMAGE_PATHS if os.path.exists(p)), None)
        if not path:
            messagebox.showerror("Error", "s2.png not found!")
            self.root.destroy()
            return None
        return ImageTk.PhotoImage(Image.open(path).resize((1920, 1080)))

    def _find_student(self, query):
        """Return the Student object (case-insensitive) or None"""
        query = query.strip().lower()
        return next((s for s in self.students
                     if s.sid.lower() == query or query in s.name.lower()), None)

    # View_all shows a formatted table of all students with averages;
    # view_individual searches by ID or name and displays a detailed record; 
    # and show_highest and show_lowest identify and display the top and bottom performers by total marks—all of which use typewriter animation to present results in the chalkboard output box.
    # These are one of the main menu functions that are established.

    def view_all(self):
        if not self.students:
            self.typewrite_text("No student records found.")
            return
        text = f"{'ID':<6}{'Name':<20}{'CW':>6}{'Exam':>7}{'Total':>8}{'%':>8}{'Grade':>7}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for s in self.students:
            text += f"{s.sid:<6}{s.name:<20}{s.coursework_total:>6}{s.exam:>7}{s.total:>8}{s.percentage:7.1f}%{s.grade:>8}\n"
        avg = sum(s.percentage for s in self.students) / len(self.students)
        text += f"\nTotal Students: {len(self.students)}\nClass Average: {avg:.2f}%"
        self.typewrite_text(text)

    def view_individual(self):
        if not self.students:
            self.typewrite_text("No student data found.")
            return
        query = simpledialog.askstring("Search Student", "Enter Student ID or Name:")
        if not query:
            return
        found = self._find_student(query)
        if found:
            self.typewrite_text(found.formatted())
        else:
            self.typewrite_text(f"No student found for '{query.capitalize()}'")

    def show_highest(self):
        if not self.students:
            self.typewrite_text("No data available.")
            return
        top = max(self.students, key=lambda s: s.total)
        result = "             HIGHEST OVERALL MARK             \n\n" + top.formatted()
        self.typewrite_text(result)

    def show_lowest(self):
        if not self.students:
            self.typewrite_text("No data available.")
            return
        low = min(self.students, key=lambda s: s.total)
        result = "             LOWEST OVERALL MARK              \n\n" + low.formatted()
        self.typewrite_text(result)

    # After sorting the in-memory student list by total marks using a modal dialogue with radio buttons to allow the user to select ascending or descending order,
    #  the sort_records method uses the view_all table format to display the results.

    def sort_records(self):
        if not self.students:
            self.typewrite_text("No records to sort.")
            return

        order_win = tk.Toplevel(self.root)
        order_win.title("Sort Order")
        order_win.geometry("300x150")
        order_win.transient(self.root)
        order_win.grab_set()

        var = tk.StringVar(value="asc")
        tk.Label(order_win, text="Choose sort order:", font=("Arial", 12)).pack(pady=10)
        tk.Radiobutton(order_win, text="Ascending", variable=var, value="asc").pack()
        tk.Radiobutton(order_win, text="Descending", variable=var, value="desc").pack()

        def do_sort():
            reverse = (var.get() == "desc")
            self.students.sort(key=lambda s: s.total, reverse=reverse)
            order_win.destroy()
            self.view_all()          

        tk.Button(order_win, text="OK", command=do_sort).pack(pady=10)

    # In order to gather a new student's ID, name, three coursework marks, and exam mark, the add_record method opens a modal form. 
    # It then validates the input (e.g., marks within range), creates a Student object, adds it to the in-memory list, saves it to a file,
    #  and uses a typewriter-animated message to confirm success.

    def add_record(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Student")
        win.geometry("380x340")
        win.transient(self.root)
        win.grab_set()

        entries = {}
        labels = ["Student ID:", "Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam mark:"]
        for i, txt in enumerate(labels):
            tk.Label(win, text=txt, anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            e = tk.Entry(win, width=30)
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[txt] = e

        def submit():
            try:
                sid   = entries["Student ID:"].get().strip()
                name  = entries["Name:"].get().strip()
                c1    = int(entries["Coursework 1:"].get())
                c2    = int(entries["Coursework 2:"].get())
                c3    = int(entries["Coursework 3:"].get())
                exam  = int(entries["Exam mark:"].get())

                if not sid or not name:
                    raise ValueError("ID and Name are required.")
                if any(m < 0 or m > 50 for m in (c1, c2, c3)):
                    raise ValueError("Coursework marks must be 0-50.")
                if exam < 0 or exam > 100:
                    raise ValueError("Exam mark must be 0-100.")

                new_student = Student(sid, name, c1, c2, c3, exam)
                self.students.append(new_student)
                if save_students(self.students):
                    win.destroy()
                    self.typewrite_text(f"Student {name} ({sid}) added successfully!")
                else:
                    messagebox.showerror("Error", "Could not write to file.")
            except Exception as exc:
                messagebox.showerror("Invalid input", str(exc))

        tk.Button(win, text="Add", command=submit).grid(row=6, column=0, columnspan=2, pady=15)

    # The delete_record method asks the user for the student's name or ID, locates the record that matches,
    # displays a typewriter-animated error or confirmation, removes the student from the in-memory list, and confirms deletion with a dialogue.

    def delete_record(self):
        if not self.students:
            self.typewrite_text("No records to delete.")
            return

        query = simpledialog.askstring("Delete Student", "Enter Student ID or Name:")
        if not query:
            return
        student = self._find_student(query)
        if not student:
            self.typewrite_text(f"No student found for '{query}'")
            return

        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete {student.name} ({student.sid})?"):
            return

        self.students = [s for s in self.students if s.sid != student.sid]
        if save_students(self.students):
            self.typewrite_text(f"Student {student.name} removed.")
        else:
            messagebox.showerror("Error", "Failed to update file.")

    # After asking the user to select a student, the update_record method opens a submenu with checkboxes to select which fields to edit, 
    # gathers new values through validation-enabled input dialogues, updates the student object in memory, persists changes to the file,
    # and provides a typewriter-animated message to confirm success.

    def update_record(self):
        if not self.students:
            self.typewrite_text("No records to update.")
            return

        query = simpledialog.askstring("Update Student", "Enter Student ID or Name:")
        if not query:
            return
        student = self._find_student(query)
        if not student:
            self.typewrite_text(f"No student found for '{query}'")
            return

        sub = tk.Toplevel(self.root)
        sub.title(f"Update {student.name}")
        sub.geometry("420x380")
        sub.transient(self.root)
        sub.grab_set()

        vars_ = {}
        fields = [
            ("Student ID", "sid", lambda: student.sid),
            ("Name",       "name", lambda: student.name),
            ("CW 1",       "cw1", lambda: student.coursework[0]),
            ("CW 2",       "cw2", lambda: student.coursework[1]),
            ("CW 3",       "cw3", lambda: student.coursework[2]),
            ("Exam",       "exam", lambda: student.exam),
        ]

        for i, (label, _, getter) in enumerate(fields):
            var = tk.BooleanVar()
            vars_[label] = var
            chk = tk.Checkbutton(sub, text=f"{label}:  {getter()}", variable=var)
            chk.grid(row=i, column=0, sticky="w", padx=15, pady=4)

        def apply_changes():
            changed = False
            try:
                if vars_["Student ID"].get():
                    new = simpledialog.askstring("New ID", "Enter new Student ID:",
                                                initialvalue=student.sid)
                    if new and new.strip():
                        student.sid = new.strip()
                        changed = True

                if vars_["Name"].get():
                    new = simpledialog.askstring("New Name", "Enter new Name:",
                                                initialvalue=student.name)
                    if new and new.strip():
                        student.name = new.strip()
                        changed = True

                if vars_["CW 1"].get():
                    new = simpledialog.askinteger("CW 1", "New mark (0-50):",
                                                 minvalue=0, maxvalue=50,
                                                 initialvalue=student.coursework[0])
                    if new is not None:
                        student.coursework[0] = new
                        changed = True

                if vars_["CW 2"].get():
                    new = simpledialog.askinteger("CW 2", "New mark (0-50):",
                                                 minvalue=0, maxvalue=50,
                                                 initialvalue=student.coursework[1])
                    if new is not None:
                        student.coursework[1] = new
                        changed = True

                if vars_["CW 3"].get():
                    new = simpledialog.askinteger("CW 3", "New mark (0-50):",
                                                 minvalue=0, maxvalue=50,
                                                 initialvalue=student.coursework[2])
                    if new is not None:
                        student.coursework[2] = new
                        changed = True

                if vars_["Exam"].get():
                    new = simpledialog.askinteger("Exam", "New mark (0-100):",
                                                 minvalue=0, maxvalue=100,
                                                 initialvalue=student.exam)
                    if new is not None:
                        student.exam = new
                        changed = True

                if changed and save_students(self.students):
                    sub.destroy()
                    self.typewrite_text(f"Record for {student.name} updated.")
                elif not changed:
                    sub.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(sub, text="Apply Changes", command=apply_changes).grid(row=len(fields),
                                                                        column=0, pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()