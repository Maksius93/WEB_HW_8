from mongoengine import connect, Document
from mongoengine.fields import StringField, BooleanField
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

class Task(Document):
    completed = BooleanField(default=False)
    consumer = StringField()
    email = StringField()