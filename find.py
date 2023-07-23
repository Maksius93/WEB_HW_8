import configparser
import models
import re
import redis
from mongoengine import connect, Document, StringField, ListField
from redis_lru import RedisLRU


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def main():
    print("Welcome to the Quotes Search Script!")
    print("Enter 'exit' to quit the script.")

    while True:
        command = input("Enter your command: ")
        if command == 'exit':
            print("Goodbye!")
            break

        if command.startswith('name:'):
            author_name = command.split('name:')[1].strip()
            authors = models.Author.objects(fullname__istartswith=author_name).first()
            results = models.Quote.objects(author=authors.id)
        elif command.startswith('tag:'):
            tag_name = command.split('tag:')[1].strip()
            tag_regex = re.compile(f'.*{tag_name}.*', re.IGNORECASE)
            results = models.Quote.objects(tags=tag_regex)
        elif command.startswith('tags:'):
            tags = command.split('tags:')[1].strip().split(",")
            results = models.Quote.objects(tags__in=tags)
        else:
            print("Invalid command. Please try again.")
            continue

        if results:
            print("Results:")
            for result in results:
                print(result.to_mongo().to_dict())
        else:
            print("No results found.")


if __name__ == "__main__":
    main()
