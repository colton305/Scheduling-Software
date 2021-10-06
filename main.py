
import pymongo
import requests
from bs4 import BeautifulSoup

from _class import _Class
from course import Course
from subject import Subject

HEADERS = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
RESPONSE = requests.get("https://apps.ualberta.ca/catalogue/faculty/sc", headers=HEADERS)
SOUP = BeautifulSoup(RESPONSE.content, features="html.parser")


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    subject_collection = db["subjects"]
    course_collection = db["courses"]
    class_collection = db["classes"]

    subjects = []
    for subject in SOUP.find("div", class_="col-md-6").findAll("a"):
        subject_url = "https://apps.ualberta.ca" + subject["href"]
        subject_response = requests.get(subject_url, headers=HEADERS)
        subject_soup = BeautifulSoup(subject_response.content, features="html.parser")
        subjects.append(Subject("Faculty of Science", subject_soup))
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


if __name__ == "__main__":
    main()
