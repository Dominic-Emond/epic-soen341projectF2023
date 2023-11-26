from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

# Testing favourite API Endpoints
def test_favourite():

    # Post
    sample_favourite = {
        "PropertyId": 1,
        "ClientId": 1
    }

    response = client.post("/favourite", json=sample_favourite)

    assert response.status_code == 200

    favourite_id = response.json().get('Id')
    assert isinstance(favourite_id, int)

    # Get
    response = client.get(f"favourite/{favourite_id}")
    assert response.status_code == 200

    fav_property_Id = response.json().get('PropertyId')
    assert fav_property_Id == 1

    # Put
    sample_favourite["PropertyId"] = 2

    response = client.put(f"favourite/{favourite_id}", json=sample_favourite)
    assert response.status_code == 200

    response = client.get(f"favourite/{favourite_id}")
    fav_property_Id = response.json().get('PropertyId')
    assert fav_property_Id == 2

    # Delete
    response = client.delete(f"favourite/{favourite_id}")
    assert response.status_code == 200