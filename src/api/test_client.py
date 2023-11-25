from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

# Testing Client API Endpoints
def test_client():
    
    # Post
    sample_client = {
        "First_Name": "Jake",
        "Last_Name": "Barnes",
        "Type": 1,
        "Username": "jake_barnes",
        "Pass": "password123"
    }

    response = client.post("/client", json=sample_client)

    assert response.status_code == 200

    client_id = response.json().get('Id')
    assert isinstance(client_id, int)

    # Get
    response = client.get(f"/client/{client_id}")
    assert response.status_code == 200

    client_name = response.json().get('First_Name')
    assert client_name == 'Jake'

    # Put
    sample_client["First_Name"] = "Jakey"

    response = client.put(f"/client/{client_id}", json=sample_client)
    assert response.status_code == 200

    response = client.get(f"/client/{client_id}")
    client_name = response.json().get('First_Name')
    assert client_name == 'Jakey'

    # Delete
    response = client.delete(f"/client/{client_id}")
    assert response.status_code == 200
