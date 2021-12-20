
import pymongo

from database_construction import construct_database
from schedule_generation.schedule import Schedule


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    for i in range(3):
        schedule = Schedule(db, "Fall")
        schedule.generate_schedule(i)


if __name__ == "__main__":
    main()
