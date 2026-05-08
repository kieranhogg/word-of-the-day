import json
from pathlib import Path
import random

import click

@click.command()

def list_files():
    dir = Path("data")
    categories = ["easy", "medium", "hard", "complex"]
    category_files = [dir / f"{item}.json" for item in categories]
    words = []
    for order, category in enumerate(category_files):
        contents = json.loads(open(category).read())
        click.echo(type(contents.get("words")))
        words.extend(contents.get("words"))
    click.echo(len(words))
    with open("data/combined.json", "w") as out:
        json.dump({"words": words}, out, indent=2)
    sorted()



if __name__ == '__main__':
    list_files()