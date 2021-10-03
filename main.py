
import pymongo
import requests
from bs4 import BeautifulSoup

from _class import _Class

HEADERS = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
RESPONSE = requests.get("https://apps.ualberta.ca/catalogue/course/biol/107", headers=HEADERS)
SOUP = BeautifulSoup(RESPONSE.content, features="html.parser")


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    collection = db["classes"]

    classes = []
    for card in SOUP.findAll("div", class_="card mt-4 dv-card-flat"):
        semester = card.find("h4", class_="m-0 flex-grow-1").text.split(" ")[0]
        for div in card.findAll("div", class_="col-lg-4 col-12 pb-3"):
            classes.append(_Class("BIOL 107", semester, div))

    for _class in classes:
        _class.save_to_db(collection)


if __name__ == "__main__":
    main()
