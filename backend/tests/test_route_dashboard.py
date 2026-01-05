import pytest
from fastapi.testclient import TestClient
from index import app
from schemas import ItemResponse, TransactionResponse, RecipeResponse
from conftest import db_session
from database.database import get_db
from datetime import datetime, timedelta


def override_get_db(db_session):
    yield db_session


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_items(client):
    expiring_soon = (datetime.now() + timedelta(days=3)).date().isoformat()

    items_data = [
        {
            "name": "Açúcar",
            "measure_unity": "grama",
            "amount": 2000,
            "description": "Açúcar refinado",
            "price": 4.50,
            "price_unit": "kg"
        },
        {
            "name": "Farinha",
            "measure_unity": "grama",
            "amount": 3,
            "description": "Farinha de trigo",
            "price": 5.00,
            "price_unit": "kg"
        },
        {
            "name": "Leite",
            "measure_unity": "mililitro",
            "amount": 1000,
            "description": "Leite integral",
            "price": 5.00,
            "price_unit": "litro",
            "expiration_date": expiring_soon
        },
        {
            "name": "Sal",
            "measure_unity": "grama",
            "amount": 0,
            "description": "Sal refinado",
            "price": 2.00,
            "price_unit": "kg"
        }
    ]

    created_items = []
    for item_data in items_data:
        response = client.post("/api/items", json=item_data)
        assert response.status_code == 201
        created_items.append(ItemResponse.model_validate(response.json()))

    return created_items


@pytest.fixture
def sample_transactions(client, sample_items):
    transactions_data = [
        {
            "item_id": sample_items[0].id,
            "order_type": "entrada",
            "description": "Compra de açúcar",
            "amount": 5000.0,
            "price": 4.50
        },
        {
            "item_id": sample_items[0].id,
            "order_type": "saída",
            "description": "Uso em receita",
            "amount": 3000.0,
            "price": None
        },
        {
            "item_id": sample_items[1].id,
            "order_type": "entrada",
            "description": "Compra de farinha",
            "amount": 1000.0,
            "price": 5.00
        },
        {
            "item_id": sample_items[1].id,
            "order_type": "saída",
            "description": "Uso em receita",
            "amount": 997.0,
            "price": None
        }
    ]

    created_transactions = []
    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201
        created_transactions.append(TransactionResponse.model_validate(response.json()))

    return created_transactions


@pytest.fixture
def sample_recipe(client, sample_items):
    recipe_data = {
        "title": "Bolo Simples",
        "steps": "Misture tudo e asse por 30 minutos",
        "description": "Receita básica de bolo",
        "recipe_itens": [
            {
                "item_id": sample_items[0].id,
                "amount": 200
            },
            {
                "item_id": sample_items[1].id,
                "amount": 300
            }
        ]
    }

    response = client.post("/api/recipes", json=recipe_data)
    assert response.status_code == 201
    return RecipeResponse.model_validate(response.json())


def test_get_dashboard_data_structure(client, sample_items, sample_transactions):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()

    assert "inventory" in dashboard
    assert "transactions_30d" in dashboard
    assert "low_stock_count" in dashboard
    assert "expiring_soon_count" in dashboard
    assert "feasible_recipes_count" in dashboard


def test_dashboard_inventory_summary(client, sample_items, sample_transactions):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()
    inventory = dashboard["inventory"]

    assert "total_items" in inventory
    assert "items_with_stock" in inventory
    assert "items_out_of_stock" in inventory
    assert "total_inventory_value" in inventory

    assert inventory["total_items"] >= 4
    assert inventory["items_with_stock"] >= 3
    assert inventory["items_out_of_stock"] >= 1
    assert inventory["total_inventory_value"] > 0


def test_dashboard_transactions_summary(client, sample_items, sample_transactions):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()
    transactions = dashboard["transactions_30d"]

    assert "period" in transactions
    assert "entries" in transactions
    assert "exits" in transactions
    assert "balance" in transactions

    assert transactions["entries"]["count"] >= 2
    assert transactions["exits"]["count"] >= 2
    assert transactions["entries"]["total_value"] > 0


def test_dashboard_low_stock_count(client, sample_items, sample_transactions):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["low_stock_count"] >= 1


def test_dashboard_expiring_soon_count(client, sample_items, sample_transactions):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["expiring_soon_count"] >= 1


def test_dashboard_with_recipe(client, sample_items, sample_transactions, sample_recipe):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()

    assert "feasible_recipes_count" in dashboard
    assert dashboard["feasible_recipes_count"] >= 0


def test_dashboard_empty_database(client):
    response = client.get("/dashboard")
    assert response.status_code == 200

    dashboard = response.json()

    assert dashboard["inventory"]["total_items"] == 0
    assert dashboard["low_stock_count"] == 0
    assert dashboard["expiring_soon_count"] == 0
    assert dashboard["feasible_recipes_count"] == 0


def test_dashboard_performance(client, sample_items, sample_transactions):
    import time

    start_time = time.time()
    response = client.get("/dashboard")
    end_time = time.time()

    assert response.status_code == 200
    assert (end_time - start_time) < 2.0