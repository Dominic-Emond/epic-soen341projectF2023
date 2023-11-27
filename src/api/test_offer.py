from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

# Testing offer API Endpoints
def test_offer():

    # Post
    sample_offer = {
        "Price": 50000.0,
        "PropertyId": 1,
        "ClientId": 1,
        "BrokerId": 1
    }

    response = client.post("/offer", json=sample_offer)

    assert response.status_code == 200

    offer_id = response.json().get('Id')
    assert isinstance(offer_id, int)

    # Get
    response = client.get(f"offer/{offer_id}")
    assert response.status_code == 200

    offer_price = response.json().get('Price')
    assert offer_price == 50000.0

    # Put
    sample_offer["Price"] = 90000.0

    response = client.put(f"offer/{offer_id}", json=sample_offer)
    assert response.status_code == 200

    response = client.get(f"offer/{offer_id}")
    offer_price = response.json().get('Price')
    assert offer_price == 90000.0

    # Delete
    response = client.delete(f"offer/{offer_id}")
    assert response.status_code == 200