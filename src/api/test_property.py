from fastapi.testclient import TestClient
from main import app
import os


client = TestClient(app)

# Testing Property API Endpoints
def test_property():

    # Post
    sample_property = {
        "Address": "123 Main St",
        "City": "Anytown",
        "Price": 500000.0,
        "Bedrooms": 3,
        "Bathrooms": 2,
        "Size_SqFt": 1500.0,
        "IsAvailable": True,
        "Broker_Id": 1  
    }

    response = client.post("/property", json=sample_property)
    assert response.status_code == 200

    property_id = response.json().get('Id')
    assert isinstance(property_id, int)

    # Search
    response = client.get(f"searchproperty/{sample_property['City']}")
    assert any(record['Id'] == property_id for record in response.json())

    # Get
    response = client.get(f"/property/{property_id}")
    assert response.status_code == 200

    property_address = response.json().get('Address')
    assert property_address == '123 Main St'

    # Put
    sample_property["Address"] = "456 Oak St"

    response = client.put(f"/property/{property_id}", json=sample_property)
    assert response.status_code == 200

    response = client.get(f"/property/{property_id}")
    property_address = response.json().get('Address')
    assert property_address == '456 Oak St'

    # Delete
    response = client.delete(f"/property/{property_id}")
    assert response.status_code == 200
