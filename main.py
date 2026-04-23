from enum import Enum
import json
from datetime import datetime as dt
from functools import lru_cache
import logging
import random
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from pathlib import Path

import uvicorn

logger = logging.getLogger('uvicorn.error')

BASE_DIR = Path(__file__).resolve().parent
WORDS_PATH = BASE_DIR / "data"


app = FastAPI()
router = APIRouter(prefix="/api")

class Category(Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    complex = "complex"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Word(BaseModel):
    word: str
    definition: str
    order: int
    level: Category = Category.easy

@lru_cache(maxsize=1)
def load_all_words_from_category(level: Category) -> list:
    level_filename = f"{level.value}.json"
    with open(WORDS_PATH / level_filename, "r") as f:
        return json.load(f)["words"]
    
@lru_cache(maxsize=1)
def load_word_from_category(order: int, level: Category | None = None) -> list:
    if not level:
        level = random.choice(list(Category))
    level_filename = f"{level.value}.json"
    with open(WORDS_PATH / level_filename, "r") as f:
        full_file = json.load(f)["words"]
    line = next(word for word in full_file if word.get("order") == order)

@router.get("/words/wotd/")
def get_word(level: Annotated[Category | None, Query()] = None):
    day_of_year = dt.now().timetuple().tm_yday

    if not level:
        level = random.choice(list(Category))
    all_things = load_all_words_from_category(level=level)
    word = Word(**all_things[day_of_year])
    
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    return word


@router.get("/words/")
def words():
    return load_all_words_from_category()

@router.get("/words/random")
def random_word():
    return random.choice(load_all_words_from_category())

@router.get("/")
def home():
    response = RedirectResponse(url='/docs')
    return response 



app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)