from fastapi.staticfiles import StaticFiles
from enum import Enum
import json
from datetime import datetime as dt
from functools import lru_cache
import logging
import random
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from pathlib import Path

import uvicorn

logger = logging.getLogger("uvicorn.error")

BASE_DIR = Path(__file__).resolve().parent
WORDS_PATH = BASE_DIR / "data"


app = FastAPI()
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


class Category(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    COMPLEX = "complex"


CATEGORY_LEVELS = {
    Category.EASY: 1,
    Category.MEDIUM: 2,
    Category.HARD: 3,
    Category.COMPLEX: 4,
}
WORD_FILE = Path(WORDS_PATH / "wordlist.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_pna_header(request: Request, call_next):
    if request.method == "OPTIONS":
        response = await call_next(request)
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


class Word(BaseModel):
    word: str
    definition: str
    order: int
    level: int


@lru_cache(maxsize=1)
def load_words(level: Category | None = None) -> list:
    with open(WORD_FILE, "r") as f:
        words = json.load(f)["words"]
        if level:
            return [word for word in words if word["level"] == CATEGORY_LEVELS[level]]
        return words


@lru_cache(maxsize=1)
def load_word_from_category(order: int, level: Category) -> list:
    if not level:
        level = random.choice(list(Category))
    level_filename = f"{level.value}.json"
    with open(WORDS_PATH / level_filename, "r") as f:
        full_file = json.load(f)["words"]
    line = next(word for word in full_file if word.get("order") == order)


@app.get("/{level}")
def word_of_the_day(level: Category = Category.MEDIUM):
    day_of_year = dt.now().timetuple().tm_yday
    if not level:
        level = random.choice(list(Category))
    all_things = load_words(level=level)
    if len(all_things) < day_of_year:
        day_of_year -= len(all_things)
    word = Word(**all_things[day_of_year])

    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    return word


@app.get("/words/")
def words():
    return load_words()


@app.get("/words/random")
def random_word():
    return random.choice(load_words())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
