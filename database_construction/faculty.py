
class Faculty:

    def __init__(self, soup):
        self.faculty_id = soup.find("h2").text.split("for ")[-1]

    def __generate_dict(self):
        json = {"_id": self.faculty_id}
        return json

    def save_to_db(self, collection):
        current_faculties = collection.find({"_id": self.faculty_id})
        exists = False
        for faculty in current_faculties:
            exists = True
        if exists:
            return
        collection.insert_one(self.__generate_dict())
