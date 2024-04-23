from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_rate_limiter():
    limit = 100
    for i in range(limit):
        client.get('/students',headers={"X-id": "661b8ed3e0e626db7f351524"}) #id for dummy student
    
    response = client.get('/students',headers={"X-id": "661b8ed3e0e626db7f351524"})
    assert response.status_code == 429
    assert response.json() == {"detail":f"{limit} requests allowed per day"}
