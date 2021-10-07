
import pymongo

from database_construction import construct_database


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    construct_database(db)


if __name__ == "__main__":
    main()
