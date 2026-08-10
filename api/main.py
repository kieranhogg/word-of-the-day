from contextlib import asynccontextmanager
import json
import logging
import random
from datetime import datetime as dt
from enum import Enum
from functools import lru_cache
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger("uvicorn.error")

BASE_DIR = Path(__file__).resolve().parent
WORDS_PATH = BASE_DIR / "data"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Loaded at start-up
    try:
        with WORD_FILE.open() as f:
            all_words = json.load(f)["words"]
    except (OSError, json.JSONDecodeError, KeyError):
        logger.exception(f"Failed to load {WORD_FILE}")
        raise

    by_level: dict[Level | None, list[dict]] = {None: all_words}

    for level in Level:
        by_level[level] = [
            word for word in all_words if word.get("level") == LEVELS[level]
        ]
    app.state.words = by_level
    yield


app = FastAPI(lifespan=lifespan)


class Level(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    COMPLEX = "complex"


LEVELS = {
    Level.EASY: 1,
    Level.MEDIUM: 2,
    Level.HARD: 3,
    Level.COMPLEX: 4,
}

WORD_FILE = WORDS_PATH / "wordlist.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_pna_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


class Word(BaseModel):
    word: str
    definition: str
    order: int
    level: int
    category: str | None = None
    image: str | None = None


def _word_for_day(wordlist, day_of_year) -> Word:
    if not wordlist:
        raise HTTPException(status_code=404, detail="No words available")
    day_of_year %= len(wordlist)
    word = Word(**wordlist[day_of_year])
    return word


@app.get("/")
def random_word_of_the_day(request: Request) -> Word:
    day_of_year = dt.now().timetuple().tm_yday
    random_level_num = day_of_year % len(list(Level))
    # Get the level dict, turn the items into a list to select a random index
    random_level, _ = list(LEVELS.items())[random_level_num]
    wordlist = request.app.state.words[random_level]
    return _word_for_day(wordlist, day_of_year)


@app.get("/words/")
def words(request: Request) -> list[Word]:
    return request.app.state.words[None]


@app.get("/words/random")
def random_word(request: Request) -> Word:
    return random.choice(request.app.state.words[None])


@app.get("/{level}")
def word_of_the_day(request: Request, level: Level = Level.MEDIUM) -> Word:
    day_of_year = dt.now().timetuple().tm_yday
    return _word_for_day(request.app.state.words[level], day_of_year)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
