import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch, MagicMock
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_create_item_missing_name(client):
    response = client.post("/items", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


@patch("app.app.get_db")
def test_get_items(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = [(1, "Test Item")]
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn

    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert data["items"][0]["name"] == "Test Item"


@patch("app.app.get_db")
def test_create_item(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (42,)
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn

    response = client.post("/items", json={"name": "New Item"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New Item"
    assert data["id"] == 42
