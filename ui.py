
from custom_figures import round_rectangle
from ui_functions import *
from backend_functions import *

from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import pyglet

# Export this to ui_styles.py


class App(ttk.Frame):

    def __init__(self, master=None):
        # Initialize the settings
        super().__init__(master)
        self.master.title("Scheduling Software")
        self.master.geometry("1000x650")
        self.master.update()
        self.master.configure(bg="#E0E5EC")
        self.grid()

        # Define styles
        self.style = ttk.Style(self)
        self.style.theme_use("default")
        self.style.configure("navbar.TFrame", background="#E0E5EC", relief="raised", borderwidth=4,
                             takefocus=True)
        self.schedule_icon = Image.open("./assets/schedule_icon.png")
        self.schedule_icon = self.schedule_icon.resize((75, 75))
        self.schedule_icon = ImageTk.PhotoImage(self.schedule_icon)
        self.style.configure("course_navbar.TButton", image=self.schedule_icon, background="#E0E5EC", borderwidth=0)
        self.style.map("course_navbar.TButton", background=[("active", "#E0E5EC")])
        self.style.configure("course.TFrame", background="#E0E5EC")
        self.style.configure("course.TButton", background="#E0E5EC", font=("Montserrat", 16, "bold"), borderwidth=4,
                             relief="raised")
        self.style.map("course.TButton", background=[("active", "white")])
        self.style.configure("search.TEntry")
        self.style.configure("course_search.TFrame", background="white")
        self.style.configure("course_search.TButton", background="white", font=("Montserrat", 14, "bold"),
                             borderwidth=0)
        self.style.map("course_search.TButton", background=[("active", "white")], foreground=[("active", "green")])

        # Create the scene
        self.nav_bar = ttk.Frame(self.master, style="navbar.TFrame", padding=15)
        self.nav_bar.grid(row=0, column=0, columnspan=2, sticky=EW)
        self.course_frames = []
        self.highlight_canvas, self.highlight = None, None
        self.schedule_button = ttk.Button(self.nav_bar, style="course_navbar.TButton",
                                          command=lambda: tab_change_animation(self.nav_bar, self.highlight_canvas,
                                                                               self.highlight))
        self.schedule_button.grid(row=0)
        self.nav_bar.update()
        self.highlight_canvas = Canvas(self.nav_bar, bg="#E0E5EC", highlightthickness=0,
                                       width=self.nav_bar.winfo_width(), height=15)
        self.highlight_canvas.grid(row=1)
        self.nav_bar.update()
        self.highlight = self.highlight_canvas.create_oval(self.highlight_canvas.winfo_width()/2 - 5,
                                                           self.highlight_canvas.winfo_height()/2 - 5,
                                                           self.highlight_canvas.winfo_width()/2 + 5,
                                                           self.highlight_canvas.winfo_height()/2 + 5,
                                                           fill="blue", outline="blue")
        self.highlight_canvas.update()
        for i in range(2):
            self.course_frames.append(ttk.Frame(self.master, style="course.TFrame"))
            self.course_frames[-1].grid(row=1, column=i, sticky=N)
            self.course_canvas = Canvas(self.course_frames[-1], bg="#E0E5EC", highlightthickness=0,
                                        width=self.master.winfo_width()/2, height=self.master.winfo_height()/8)
            self.course_canvas.create_window(0, 0)
            self.course_canvas.grid(row=0, sticky=N)
            self.master.update()
            round_rectangle(self.course_canvas, self.course_canvas.winfo_width()/5,
                            self.course_canvas.winfo_height()/7, self.course_canvas.winfo_width()*4/5,
                            self.course_canvas.winfo_height()*6/7, radius=20, fill="#E0E5EC", outline="black", width=3)
            self.add_course_button = ttk.Button(self.course_frames[-1], style="course.TButton", text="+", width=2,
                                                command=lambda course_frame=self.course_frames[-1]:
                                                search_course_modal(self.master, course_frame))
            self.add_course_button.grid(row=0)


def main():
    app = App()
    app.mainloop()
