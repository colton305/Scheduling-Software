
class Course:

    def __init__(self, subject, soup):
        self.subject = subject
        header = soup.find("h2", class_="m-0").text
        self.course_id = header.split("-")[0].strip()
        self.description = header.split("-")[1].strip()
        self.credits = soup.find("h5", class_="mt-0").text.split(" ")[1]
        try:
            long_text = soup.findAll("p")[1].text
            prereq_position = long_text.find("Prerequisite")
        except IndexError:
            prereq_position = -1
        if prereq_position == -1:
            self.prereqs = None
        else:
            # Temporary prereq determination, PLS FIX LATER
            self.prereqs = []
            prereq_string = long_text[prereq_position:]
            start = 0
            end = 0
            for i, char in enumerate(prereq_string):
                if char == ":":
                    start = i
                elif char == ".":
                    end = i
                    break
            prereq_string = prereq_string[start + 2: end]
            prereq_list = prereq_string.split(" ")
            class_num = 0
            for i, word in enumerate(prereq_list):
                if i == 0:
                    subject = word
                else:
                    if len(word) > 3:
                        word = word[:4]
                    try:
                        class_num = int(word)
                    except ValueError:
                        class_num = 0
                    break
            if class_num == 0:
                self.prereqs = None
            else:
                self.prereqs.append(subject + " " + str(class_num))

    def print_stuff(self):
        print(self.subject)
        print(self.course_id)
        print(self.description)
        print(self.credits)
        print(self.prereqs)

    # Generate a dictionary of all of the course variables for saving to the database
    def __generate_dict(self):
        json = {"_id": self.course_id, "subject": self.subject, "description": self.description, "credits": self.credits,
                "prerequisites": self.prereqs}
        return json

    # Save the course to the database
    def save_to_db(self, collection):
        current_courses = collection.find({"_id": self.course_id})
        exists = False
        for _class in current_courses:
            exists = True
        if exists:
            return
        collection.insert_one(self.__generate_dict())
