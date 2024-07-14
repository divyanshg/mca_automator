from config import MONGO_URL, DATABASE_NAME
import argparse
from pymongo import MongoClient
from importer import import_data
from mailer import mail_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import data or send emails")
    parser.add_argument('command', choices=['import', 'mail'], help="Command to run: 'import' or 'mail'")
    args = parser.parse_args()

    try:
        mongoClient = MongoClient(MONGO_URL)
        db = mongoClient[DATABASE_NAME]

        if args.command == 'import':
            import_data(db)
        elif args.command == 'mail':
            mail_data(db, mongoClient)
    except Exception as e:
        print(e)
    finally:
        mongoClient.close()