import pymongo


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["scheduling"]
    print(db.list_collection_names())


if __name__ == "__main__":
    main()
