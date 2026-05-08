from fastapi.testclient import TestClient
from fastapi import status
from httpx import request
from main import app, Category, CATEGORY_LEVELS

# Initialize the test client with your app
client = TestClient(app)

KEYS = ["level", "word", "definition", "category", "order"]

def test_random_word():
    response = client.get("/words/random/")
    assert response.status_code == status.HTTP_200_OK
    assert len(KEYS) == len(response.json().keys())
    assert all([key in KEYS for key in response.json().keys()])

def test_get_word_valid_category():
    response = client.get("/complex")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("level") == CATEGORY_LEVELS[Category.COMPLEX]
    
def test_get_word_no_category():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_get_word_invalid_category():
    response = client.get("/wrong")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT