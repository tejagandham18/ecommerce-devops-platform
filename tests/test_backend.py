
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "app" / "backend")
)

from main import app


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["application"] == "E-Commerce API"
    assert data["status"] == "running"


@patch("main.get_connection")
def test_health_endpoint(mock_get_connection):
    mock_connection = MagicMock()
    mock_get_connection.return_value.__enter__.return_value = mock_connection

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "database": "connected",
    }


@patch("main.get_connection")
def test_products_endpoint(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Laptop", 55000.00),
        (2, "Headphones", 2500.00),
        (3, "Keyboard", 1500.00),
    ]

    client = app.test_client()
    response = client.get("/api/products")

    assert response.status_code == 200

    products = response.get_json()
    assert len(products) == 3
    assert products[0]["name"] == "Laptop"
    assert products[0]["price"] == 55000.0
