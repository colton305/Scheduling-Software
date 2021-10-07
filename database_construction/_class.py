
class _Class:

    def __init__(self, course, semester, soup):
        self.course = course
        self.semester = semester
        class_header = soup.find("strong", class_="mb-0 mt-4").text.strip()
        self.delivery_type = class_header.split(" ")[0]
        self.class_id = class_header.split(" ")[2].split("\n")[0].replace("(", "").replace(")", "")
        try:
            schedule = soup.find("span", class_="ms-3").text
            self.schedule_days = schedule.split(" ")[0]
            self.schedule_time = schedule.split(" ")[1] + schedule.split(" ")[2] + schedule.split(" ")[3]
        except AttributeError:
            self.schedule_days = None
            self.schedule_time = None
        self.professor = None
        for em in soup.findAll("em"):
            professor = em.find("a")
            if professor is not None:
                self.professor = professor.text

    def print_stuff(self):
        print(self.course)
        print(self.semester)
        print(self.delivery_type)
        print(self.class_id)
        print(self.schedule_days)
        print(self.schedule_time)
        print(self.professor)

    # Generate a dictionary of all of the class variables for saving to the database
    def __generate_dict(self):
        json = {"_id": self.class_id, "course": self.course, "semester": self.semester, "delivery type": self.delivery_type,
                "schedule": [self.schedule_days, self.schedule_time], "professor": self.professor}
        return json

    # Save the class to the database
    def save_to_db(self, collection):
        current_classes = collection.find({"_id": self.class_id})
        exists = False
        for _class in current_classes:
            exists = True
        if exists:
            return
        collection.insert_one(self.__generate_dict())
