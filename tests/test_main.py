from fastapi.testclient import TestClient
from fastapi import status
from api.main import app, Level, LEVELS

client = TestClient(app, base_url="http://server:8000/")

EXPECTED_KEYS = ["level", "word", "definition", "category", "order"]


def test_random_word():
    """Get a random word from the full selection."""
    response = client.get("/words/random")
    assert response.status_code == status.HTTP_200_OK
    assert len(EXPECTED_KEYS) == len(response.json().keys())
    assert all([key in EXPECTED_KEYS for key in response.json().keys()])


def test_get_word_valid_level():
    """Providing a valid level should return a valid response."""
    response = client.get(f"/{Level.COMPLEX.value}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("level") == LEVELS[Level.COMPLEX]


def test_get_word_of_the_day_no_level():
    """This should return a word with a random level for today."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_get_word_of_the_day_no_level_is_the_same():
    """Once a random level is chosen for the day, it should be the same each time."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    word = response.json()["word"]
    for _ in range(10):
        response = client.get("/")
        assert response.json()["word"] == word


def test_get_word_invalid_level():
    """Requesting an invalid level should return a 422 error."""
    response = client.get("/wrong")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
