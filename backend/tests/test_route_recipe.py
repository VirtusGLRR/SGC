import pytest
from fastapi.testclient import TestClient
from index import app
from schemas import RecipeResponse
from conftest import db_session
from database.database import get_db

def override_get_db(db_session):
    yield db_session

@pytest.fixture
def client(db_session):

    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Lasanha", "steps": "coloque a massa no forno pre aquecido", "description": "Gosto sem igual!" },
        {"title": "Frango grelhado", "steps": "coloque o frango na panela aquecida", "description": "Muito bom!" },
    ]
)
def test_create_recipe(client, payload):
    response = client.post("/api/recipes", json = payload)

    assert response.status_code == 201

    recipe_response = RecipeResponse.model_validate(response.json())

    assert recipe_response.title == payload["title"]
    assert recipe_response.steps == payload["steps"]
    assert recipe_response.description == payload["description"]
    assert recipe_response.id is not None