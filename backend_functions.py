
import pandas as pd


# Save the user's course selections to a file
def save_course_selections(frames):
    courses = {"Fall Courses": [], "Winter Courses": []}
    for i, semester in enumerate(courses.keys()):
        for slave in frames[i].grid_slaves():
            if str(type(slave)) == "<class 'tkinter.Label'>":
                courses[semester].append(slave["text"])
    df = pd.DataFrame.from_dict(courses, orient="index").transpose()
    df.to_csv("files/course_selections.csv")
