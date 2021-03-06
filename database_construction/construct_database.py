
import requests
from bs4 import BeautifulSoup

from ._class import _Class
from .course import Course
from .subject import Subject
from .faculty import Faculty

HEADERS = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
RESPONSE = requests.get("https://apps.ualberta.ca/catalogue", headers=HEADERS)
SOUP = BeautifulSoup(RESPONSE.content, features="html.parser")


# Construct the database
def construct_database(db):
    # Expects db as a MongoDB database
    faculty_collection = db["faculties"]
    subject_collection = db["subjects"]
    course_collection = db["courses"]
    class_collection = db["classes"]

    faculties = []
    for faculty in SOUP.find("div", class_="col-md-6").findAll("a"):
        faculty_url = "https://apps.ualberta.ca" + faculty["href"]
        faculty_response = requests.get(faculty_url, headers=HEADERS)
        faculty_soup = BeautifulSoup(faculty_response.content, features="html.parser")
        faculties.append(Faculty(faculty_soup))
        subjects = []
        for subject in faculty_soup.find("div", class_="col-md-6").findAll("a"):
            subject_url = "https://apps.ualberta.ca" + subject["href"]
            subject_response = requests.get(subject_url, headers=HEADERS)
            subject_soup = BeautifulSoup(subject_response.content, features="html.parser")
            subjects.append(Subject(faculties[-1].faculty_id, subject_soup))
            courses = []
            for button in subject_soup.findAll("a", class_="btn btn-sm btn-secondary"):
                course_url = "https://apps.ualberta.ca/" + button["href"]
                course_response = requests.get(course_url, headers=HEADERS)
                course_soup = BeautifulSoup(course_response.content, features="html.parser")
                courses.append(Course(subjects[-1].subject_id, course_soup))
                classes = []
                for card in course_soup.findAll("div", class_="card mt-4 dv-card-flat"):
                    semester = card.find("h4", class_="m-0 flex-grow-1").text.split(" ")[0]
                    for div in card.findAll("div", class_="col-lg-4 col-12 pb-3"):
                        classes.append(_Class(courses[-1].course_id, semester, div))

                for _class in classes:
                    _class.save_to_db(class_collection)
            for course in courses:
                course.save_to_db(course_collection)
        for subject in subjects:
            subject.save_to_db(subject_collection)
    for faculty in faculties:
        faculty.save_to_db(faculty_collection)
