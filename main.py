
import pymongo
import requests
from bs4 import BeautifulSoup

from _class import _Class
from course import Course

HEADERS = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
RESPONSE = requests.get("https://apps.ualberta.ca/catalogue/course/biol", headers=HEADERS)
SOUP = BeautifulSoup(RESPONSE.content, features="html.parser")


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    course_collection = db["courses"]
    class_collection = db["classes"]

    courses = []
    for button in SOUP.findAll("a", class_="btn btn-sm btn-secondary"):
        url = "https://apps.ualberta.ca/" + button["href"]
        course_response = requests.get(url, headers=HEADERS)
        course_soup = BeautifulSoup(course_response.content, features="html.parser")
        courses.append(Course("BIOL", course_soup))
        classes = []
        for card in course_soup.findAll("div", class_="card mt-4 dv-card-flat"):
            semester = card.find("h4", class_="m-0 flex-grow-1").text.split(" ")[0]
            for div in card.findAll("div", class_="col-lg-4 col-12 pb-3"):
                classes.append(_Class(courses[-1].course_id, semester, div))

        for _class in classes:
            _class.save_to_db(class_collection)
    for course in courses:
        course.save_to_db(course_collection)


if __name__ == "__main__":
    main()
