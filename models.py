from mongoengine import connect, Document
from mongoengine.fields import StringField, ReferenceField, ListField
import configparser
import json


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField(max_length=5000)


class Qoute(Document):
    quote = StringField(max_length=220, required=True)
    author = ReferenceField(Author)
    tags = ListField(StringField(max_length=30))


if __name__ == '__main__':
    with open ("authors.json", "r") as file:
        data = json.load(file)

    for item in data:
        author = Author(**item)
        author.save()

    with open ("qoutes.json", "r") as file:
        data = json.load(file)

    for item in data:
        qoute = Qoute(**item)
        qoute.save()