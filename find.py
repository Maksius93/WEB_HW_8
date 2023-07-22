import configparser
from mongoengine import connect, Document, StringField, ListField
import models
import re

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

def search_quotes(query):
    # Знаходимо автора за іменем
    authors = models.Author.objects(fullname__icontains=query)

    if authors:
        # Знайдено автора, знаходимо його цитати
        author = authors.first()
        results = models.Qoute.objects.filter(author=author)

        if results:
            # Виводимо всі цитати зі списку знайдених цитат
            for quote in results:
                print(quote.to_mongo().to_dict())
        else:
            print("No results found.")
    else:
        print("Author not found.")


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
            search_quotes(author_name)
        elif command.startswith('tag:'):
            tag_name = command.split('tag:')[1].strip()
            tag_regex = re.compile(f'.*{tag_name}.*', re.IGNORECASE)
            results = models.Qoute.objects(tags=tag_regex)
        elif command.startswith('tags:'):
            tags = command.split('tags:')[1].strip().split(",")
            results = models.Qoute.objects(tags__in=tags)
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
