from unicodedata import decimal
import xerox
import re
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import os
from dotenv import load_dotenv


def add_place(name, description, latitude, longitude, category='none'):
    """Creates and inserts a new document in a MongoDB collection with provided details"""
    lat = float(latitude)
    lon = float(longitude)

    client = MongoClient(os.getenv('MONGODB_URL'))
    db = client[os.getenv('MONGODB_DB_NAME')]

    point = {
        'name': name,
        'description': description,
        'category': category,
        'position': {
            'type': 'Point',
            'coordinates': [lon, lat]
        }
    }
    try:
        db.points.insert_one(point)
    except OperationFailure as op:
        print(op.details['errmsg'])


def get_input(prompt, min_characters=5, allow_null=False):
    """Get's the user's input with some validation helpers"""
    if allow_null:
        return input("{0}: ".format(prompt))

    val = input("{0}: ".format(prompt))
    while len(val) < min_characters:
        print("Need at least {0} characters.".format(min_characters))
        val = input("{0}: ".format(prompt))

    return val


def main():
    coords = xerox.paste()

    match = re.search(
        r"^((\-?|\+?)?\d+(\.\d+)?),\s*((\-?|\+?)?\d+(\.\d+)?)$", coords)
    if match is None:
        print("No coordinates found on the clipboard. Exiting.")
        quit()

    load_dotenv()

    latitude, longitude = [c.strip() for c in coords.split(',')]

    name = get_input("Name this place")
    description = get_input("Provide a description", min_characters=10)
    category = get_input("Category", allow_null=True)

    add_place(name, description, latitude, longitude, category)


if __name__ == "__main__":
    main()
