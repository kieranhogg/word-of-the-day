import json
from datetime import datetime as dt
from functools import lru_cache
import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Word(BaseModel):
    name: str
    definition: str

@lru_cache(maxsize=1)
def load_things() -> list:
    with open("data/words.json", "r") as f:
        return json.load(f)["words"]

@app.get("/words/wotd/")
def get_word():
    today = int(dt.now().strftime("%-j"))
    all_things = load_things()
    word = all_things[today]
    
    if not word:
        raise HTTPException(status_code=404, detail="Thing not found")
    
    return word


@app.get("/words/")
def words():
    return load_things()

@app.get("/words/random")
def random_word():
    return random.choice(load_things())