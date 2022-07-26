import pytest
import json
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Still Alive"}


def test_get_empty_data_trgm():
    response = client.get("/trgm?term=")
    assert response.status_code == 200
    assert response.json() == "Sonuç Bulunamadı"


def test_get_empty_data_ts():
    response = client.get("/fts?term=")
    assert response.status_code == 200
    assert response.json() == "Sonuç Bulunamadı"


def test_get_data_trgm():
    response = client.get("/trgm?term=baba")
    assert response.status_code == 200
    assert response.json() != []


def test_get_data_ts():
    response = client.get("/fts?term=baba")
    assert response.status_code == 200
    assert response.json() != []
