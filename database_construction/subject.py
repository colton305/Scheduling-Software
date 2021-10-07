
class Subject:

    def __init__(self, faculty, soup):
        self.faculty = faculty
        self.subject_id = soup.find("h2").text.split("-")[-1].strip()

    def print_stuff(self):
        print(self.faculty)
        print(self.subject_id)

    def __generate_dict(self):
        json = {"_id": self.subject_id, "faculty": self.faculty}
        return json

    def save_to_db(self, collection):
        current_subjects = collection.find({"_id": self.subject_id})
        exists = False
        for subject in current_subjects:
            exists = True
        if exists:
            return
        collection.insert_one(self.__generate_dict())
