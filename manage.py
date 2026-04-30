import json
from pathlib import Path
import random

import click

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')

# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo(f"Hello {name}!")


def list_files():
    dir = Path("data")
    categories = ["easy", "medium", "hard", "complex"]
    category_files = [dir / f"{item}.json" for item in categories]
    for order, category in enumerate(category_files):
        order += 1
        contents = json.loads(open(category).read())
        words = len(contents.get("words"))
        click.echo(f"{order}: {category} ({words} words)")
    word_file = click.prompt("View file", type=int)
    view_words(categories[word_file - 1])

def view_words(word_file):
    contents = json.loads(open(Path("data") / f"{word_file}.json").read())
    words = contents.get("words")
    random.shuffle(words)
    toggle_ids = []
    for i, word in enumerate(words):
        click.echo(f"{i + 1}: {word}")
        if i % 10 == 9:
            toggle = input()
            if toggle == "-1":
                break
            while len(toggle) > 0:
                 toggle_ids.append(toggle)
                 toggle = input()
    print(toggle_ids)

if __name__ == '__main__':
    list_files()