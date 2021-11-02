
from tkinter import *
from tkinter import ttk
import re
import time


from db import DB
from custom_figures import *


# Create a modal to search and select a course
def search_course_modal(master, frame):
    search_box = Toplevel(master)
    search_box.geometry("300x400")
    search_box.resizable(False, False)
    search_box.config(bg="white")

    search_frame = ttk.Frame(search_box, style="course_search.TFrame")
    search_frame.grid(row=0, pady=(0, 15))
    label1 = Label(search_frame, text="Search Courses:", font=("Montserrat", 12), bg="white")
    label1.grid(row=0, column=0, padx=(5, 15))
    search_box.update()
    search_entry = ttk.Entry(search_frame, font=("Montserrat", 12),
                             width=int((search_box.winfo_width() - label1.winfo_width())/12))
    search_entry.grid(row=0, column=1)
    search_entry.bind("<Return>", lambda event: query_courses(master, frame, search_box, search_entry.get()))
    search_entry.focus_set()


# Occurs when the user presses enter on the search box, queries the database for similar courses
def query_courses(master, frame, modal, search_parameter):
    for slave in modal.grid_slaves():
        if str(type(slave.grid_slaves()[0])) == "<class 'tkinter.ttk.Entry'>":
            continue
        slave.destroy()
    query_results = 0
    subject_match = re.compile("(\w)+").match(search_parameter)
    if subject_match is not None:
        subject = subject_match.group()
    else:
        subject = ""
    course_num_match = re.compile("(\d)+").search(search_parameter)
    if course_num_match is not None:
        course_num = course_num_match.group()
    else:
        course_num = ""
    query = {"_id": {"$regex": "(?i)" + subject + "[a-zA-Z]*(\s)*(\d)*" + course_num}}
    results = DB["courses"].find(query)
    course_tabs = []
    for result in results:
        if len(course_tabs) < 8:  # Most you can fit
            course_tabs.append(ttk.Frame(modal, style="course_search.TFrame"))
            course_tabs[-1].grid(row=len(course_tabs), sticky=EW)
            course_name = Label(course_tabs[-1], text=result["_id"], font=("Montserrat", 16, "bold"), bg="white")
            course_name.grid(row=0, column=0, padx=15, pady=(0, 15))
            modal.update()
            course_select = ttk.Button(course_tabs[-1], style="course_search.TButton", text="+", width=2,
                                       command=lambda course=result: add_selected_course(master, frame, modal, course))
            course_select.grid(row=0, column=1, padx=(225 - course_name.winfo_width(), 0), pady=(0, 15))


# Add the course that was selected in the modal to the master window
def add_selected_course(master, frame, modal, course_meta_data):
    modal.destroy()
    num_courses = 0
    # Destroy the button and check how many canvases there are
    for slave in frame.grid_slaves():
        if str(type(slave)) == "<class 'tkinter.ttk.Button'>":
            slave.destroy()
            continue
        num_courses += str(type(slave)) == "<class 'tkinter.Canvas'>"
    course_label = Label(frame, text=course_meta_data["_id"], font=("Helvetica", 18, "bold"), bg="#E0E5EC")
    course_label.grid(row=num_courses - 1)
    if num_courses < 5:
        update_course_display(master, frame, num_courses)


# Add a new box to insert an additional course
def update_course_display(master, frame, course_num):
    course_canvas = Canvas(frame, bg="#E0E5EC", highlightthickness=0,
                           width=master.winfo_width() / 2, height=master.winfo_height() / 8)
    course_canvas.create_window(0, 0)
    course_canvas.grid(row=course_num)
    master.update()
    round_rectangle(course_canvas, course_canvas.winfo_width() / 5,
                    course_canvas.winfo_height() / 7, course_canvas.winfo_width() * 4 / 5,
                    course_canvas.winfo_height() * 6 / 7, radius=20, fill="#E0E5EC", outline="black", width=3)
    add_course_button = ttk.Button(frame, style="course.TButton", text="+", width=2,
                                   command=lambda: search_course_modal(master, frame))
    add_course_button.grid(row=course_num)


def tab_change_animation(master, canvas, highlight):
    for i in range(30):
        increment = -0.04178 * i * (i - 30)
        canvas.move(highlight, increment, 0)
        master.update()
        time.sleep(0.01667)
