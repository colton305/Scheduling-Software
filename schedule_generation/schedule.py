
import pandas as pd
from random import choice

DAYS = {"M": "Monday", "T": "Tuesday", "W": "Wednesday", "H": "Thursday", "F": "Friday"}
EVEN_DAYS_START = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "18:00"]
ODD_DAYS_START = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "18:00"]
EVEN_DAYS_END = ["08:50", "09:50", "10:50", "11:50", "12:50", "13:50", "14:50", "15:50", "16:50", "21:00"]
ODD_DAYS_END = ["09:20", "10:50", "12:20", "13:50", "15:20", "16:50", "21:00"]


class Schedule:

    def __init__(self, db, semester, times_blocked=None, gaps_penalty=4, max_classes=3):
        # Initialize a Schedule
        # - times_blocked expects a dict with M-F as keys containing lists of blocked times
        # - gaps_penalty expects a negative int that represents the penalty for gaps
        # - maximum_classes expects an int that represents the maximum number of consecutive classes
        self.db = db
        self.semester = semester
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.schedule = {}
        if times_blocked:
            for key in times_blocked.keys():
                days.remove(key)
                self.schedule[key] = times_blocked[key]
        for i, day in enumerate(days):
            # Dope formula that assigns odd numbers 8 and even numbers 10
            self.schedule[day] = [None for j in range(-2 * (i % 2) + 10)]
        # Define the vars
        self.gaps_penalty = gaps_penalty
        self.max_classes = max_classes
        self.classes_penalty = 4
        self.possible_classes = self.__find_possible_classes()
        self.classes = []
        self.score = 0

    def __find_possible_classes(self):
        # - returns a dict containing all possible classes for each user-selected course
        # Convert the csv to a list
        df = pd.read_csv("files/course_selections.csv")
        courses = list(df[self.semester + " Courses"])
        # Use the lists to query the database
        classes = self.__query_course_db(courses)
        return classes

    def __query_course_db(self, courses):
        # - returns a dict of classes for each course
        classes = {}
        for course in courses:
            query = {"course": course, "semester": self.semester, "delivery type": "LECTURE"}
            results = self.db["classes"].find(query)
            classes[course] = []
            for result in results:
                classes[course].append(result)
        return classes

    def randomize_classes(self):
        # Randomly select classes from self.possible_classes
        # Convert classes keys to a list of courses
        courses = list(self.possible_classes.keys())
        while courses:
            # Randomly select a course and then remove it
            current_course = choice(courses)
            courses.remove(current_course)
            # Randomly select a class (check for availability) and remove it
            unavailable = True
            while unavailable:
                if self.possible_classes[current_course]:
                    _class = choice(self.possible_classes[current_course])
                    self.possible_classes[current_course].remove(_class)
                else:
                    break
                # Find when the class starts and ends
                if not _class["schedule"][1]:  # Make sure the class has a time
                    continue
                start_time = _class["schedule"][1].split("-")[0]
                end_time = _class["schedule"][1].split("-")[1]
                if not list(DAYS.keys()).index(_class["schedule"][0][0]) % 2:
                    start_time = EVEN_DAYS_START.index(start_time)
                    end_time = EVEN_DAYS_END.index(end_time)
                else:
                    start_time = ODD_DAYS_START.index(start_time)
                    end_time = ODD_DAYS_END.index(end_time)
                unavailable = False
                for day in _class["schedule"][0]:
                    # Check for availability
                    for i in range(start_time, end_time + 1):
                        if self.schedule[DAYS[day]][i]:
                            unavailable = True
                    if unavailable:
                        break
                else:
                    for day in _class["schedule"][0]:
                        for i in range(start_time, end_time + 1):
                            self.schedule[DAYS[day]][i] = _class["course"]
                    self.classes.append(_class)

    def convert_schedule(self, path):
        # Convert self.schedule to a csv
        # - path is the filename as a str
        df = pd.DataFrame.from_dict(self.schedule, orient="index").transpose()
        df.to_csv(path)

    def calculate_score(self):
        # Calculate the generated schedule's score based on scoring factors
        # - returns the score for the current schedule
        score = 100  # 100 is the starting score, the score is subsequently decremented by each negative factor
        for day in self.schedule.keys():
            # Iterate through each day in the schedule
            gaps = None
            consecutive_classes = 0
            for time in self.schedule[day]:
                # Gaps and max classes check
                if time:
                    consecutive_classes += 1
                    if not gaps:
                        gaps = 0
                    else:
                        score -= self.gaps_penalty ** gaps
                        gaps = 0
                else:
                    if consecutive_classes > self.max_classes:
                        score -= self.classes_penalty ** (consecutive_classes - self.max_classes)
                    consecutive_classes = 0
                    if gaps is not None:
                        gaps += 1
        return score

    def find_better_class(self):
        # Try to find a class that improves the schedule score for each course
        # - returns whether this function altered the schedule
        altered = False
        for i in range(len(self.classes)):
            current_course = self.classes[i]["course"]
            improved = False
            while not improved:
                # Select a new class from self.possible_classes and remove it (make sure self.possible_classes exists)
                if self.possible_classes[current_course]:
                    _class = choice(self.possible_classes[current_course])
                    self.possible_classes[current_course].remove(_class)
                else:
                    break
                # Clear the old course from the schedule
                for key in self.schedule.keys():
                    for j, time in enumerate(self.schedule[key]):
                        if time == current_course:
                            self.schedule[key][j] = None
                # Find when the class starts and ends
                if not _class["schedule"][1]:  # Make sure the class has a time
                    continue
                start_time = _class["schedule"][1].split("-")[0]
                end_time = _class["schedule"][1].split("-")[1]
                if not list(DAYS.keys()).index(_class["schedule"][0][0]) % 2:
                    start_time = EVEN_DAYS_START.index(start_time)
                    end_time = EVEN_DAYS_END.index(end_time)
                else:
                    start_time = ODD_DAYS_START.index(start_time)
                    end_time = ODD_DAYS_END.index(end_time)
                unavailable = False
                for day in _class["schedule"][0]:
                    # Check for availability
                    for j in range(start_time, end_time + 1):
                        if self.schedule[DAYS[day]][j]:
                            unavailable = True
                    if unavailable:
                        break
                else:  # Execute if the loop wasn't broken (class is available)
                    # Append the new class to the schedule
                    for day in _class["schedule"][0]:
                        for j in range(start_time, end_time + 1):
                            self.schedule[DAYS[day]][j] = _class["course"]
                    # Compare scores
                    new_score = self.calculate_score()
                    if new_score > self.score:
                        # Replace the previous class with the better one
                        self.classes[i] = _class
                        self.score = new_score
                        altered = True
                    else:
                        # If the new class was not better, erase it from the schedule and replace it with the old one
                        # Erase the bad course
                        for key in self.schedule.keys():
                            for j, time in enumerate(self.schedule[key]):
                                if time == current_course:
                                    self.schedule[key][j] = None
                # Repair the schedule using the optimal class
                start_time = self.classes[i]["schedule"][1].split("-")[0]
                end_time = self.classes[i]["schedule"][1].split("-")[1]
                if not list(DAYS.keys()).index(self.classes[i]["schedule"][0][0]) % 2:
                    start_time = EVEN_DAYS_START.index(start_time)
                    end_time = EVEN_DAYS_END.index(end_time)
                else:
                    start_time = ODD_DAYS_START.index(start_time)
                    end_time = ODD_DAYS_END.index(end_time)
                # Append the better course
                for day in self.classes[i]["schedule"][0]:
                    for j in range(start_time, end_time + 1):
                        self.schedule[DAYS[day]][j] = current_course
        return altered

    def generate_schedule(self, schedule_num):
        # Generate a schedule from scratch
        # - self is the schedule to be generated
        # - schedule_num is an int that represents the number of the schedule to be generated (for file storage)
        self.randomize_classes()
        self.set_score(self.calculate_score())
        repeat = True
        while repeat and self.get_score() != 100:
            repeat = self.find_better_class()
        self.convert_schedule("files/schedule" + str(schedule_num) + ".csv")

    def get_score(self):
        # Getter method to get the Schedule's score
        return self.score

    def set_score(self, score):
        # Setter method to set the Schedule's score
        self.score = score
