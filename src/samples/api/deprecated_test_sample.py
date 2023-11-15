from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app
import os

client = TestClient(app)

# Testing Broker API Endpoints
def test_broker():

    # Testing Access to environment variables
    load_dotenv()
    test_var = os.getenv("TEST")
    assert test_var == "123"


    # Post
    sample_broker = {
        "First_Name": "Harry",
        "Last_Name": "Potter",
        "Email_Address": "harrypotter@temp.com",
        "Username": "harry",
        "Password": "potter123"
    }

    response = client.post("/brokers", json=sample_broker)
    assert response.status_code == 200

    broker_id = response.json().get('Id')
    assert isinstance(broker_id, int)

    # Get
    response = client.get(f"brokers/{broker_id}")
    assert response.status_code == 200

    broker_name = response.json().get('First_Name')
    assert broker_name == 'Harry'

    # Put
    sample_broker["First_Name"] = "Henrietta"

    response = client.put(f"brokers/{broker_id}", json=sample_broker)
    assert response.status_code == 200

    response = client.get(f"brokers/{broker_id}")
    broker_name = response.json().get('First_Name')
    assert broker_name == 'Henrietta'

    # Delete
    response = client.delete(f"brokers/{broker_id}")
    assert response.status_code == 200