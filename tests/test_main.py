import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.main import LEVELS, Level, app

EXPECTED_KEYS = ["level", "word", "definition", "category", "order", "image"]


@pytest.fixture
def client():
    app.state.words = {
        Level.EASY: [
            {
                "word": "giggle",
                "definition": "a happy laugh sound",
                "category": "Action & Movement",
                "order": 1,
                "level": 1,
            },
        ],
        Level.MEDIUM: [
            {
                "word": "twinkle",
                "definition": "to shine with a flickering light",
                "category": "Space & Science",
                "order": 1,
                "level": 2,
            },
        ],
        Level.HARD: [
            {
                "word": "dinosaur",
                "definition": "giant animal that lived long ago",
                "category": "Animals & Nature",
                "order": 1,
                "level": 2,
            }
        ],
        Level.COMPLEX: [
            {
                "word": "nebula",
                "definition": "colorful cloud of dust and gas in space",
                "category": "Space & Science",
                "order": 1,
                "level": 4,
            }
        ],
    }
    app.state.words[None] = app.state.words[Level.EASY]
    return TestClient(app)


def test_random_word(client):
    """Get a random word from the full selection."""
    response = client.get("/words/random")
    assert response.status_code == status.HTTP_200_OK
    assert len(EXPECTED_KEYS) == len(response.json().keys())
    assert all(key in EXPECTED_KEYS for key in response.json())


def test_get_word_valid_level():
    """Providing a valid level should return a valid response."""
    with TestClient(app) as client:
        response = client.get(f"/{Level.COMPLEX.value}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("level") == LEVELS[Level.COMPLEX]


def test_get_word_of_the_day_no_level():
    """This should return a word with a random level for today."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK


def test_get_word_of_the_day_no_level_is_the_same():
    """Once a random level is chosen for the day, it should be the same each time."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        word = response.json()["word"]
        for _ in range(10):
            response = client.get("/")
            assert response.json()["word"] == word


def test_get_word_invalid_level():
    """Requesting an invalid level should return a 422 error."""
    with TestClient(app) as client:
        response = client.get("/wrong")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_lifespan_fails_on_bad_json(tmp_path, monkeypatch):
    bad_file = tmp_path / "wordlist.json"
    bad_file.write_text("not json")
    monkeypatch.setattr("api.main.WORD_FILE", bad_file)

    from api.main import app, lifespan

    with pytest.raises(json.JSONDecodeError):
        async with lifespan(app):
            pass


@pytest.mark.asyncio
async def test_lifespan_fails_on_missing_file(tmp_path, monkeypatch):
    bad_file = tmp_path / "wordlist.json"
    monkeypatch.setattr("api.main.WORD_FILE", bad_file)

    from api.main import app, lifespan

    with pytest.raises(OSError):
        async with lifespan(app):
            pass
