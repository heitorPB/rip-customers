from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_non_existent_customer():
    # insanely long id, unlikely to be in any database
    id_ = 'a'*123
    response = client.get(f'/customers/{id_}')
    assert response.status_code == 404
    assert response.json() == {'detail': f'Customer {id_} not found'}
