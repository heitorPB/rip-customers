from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_non_existent_customer():
    # insanely long id, unlikely to be in any database
    id_ = 'a'*123
    response = client.get(f'/customers/{id_}')
    assert response.status_code == 404
    assert response.json() == {'detail': f'Customer {id_} not found'}


def test_create_invalid_customer():
    body = {"first_name": "string",
            "last_name": "string",
            "email": "string",
            "gender": "string",
            "company": "string",
            "city": "string",
            "title": "string",
            "id": ""}

    response = client.post('/customers/', json=body)
    assert response.status_code == 422
    assert response.json() == {
       "detail": [
         {
           "loc": [
             "body",
             "id"
           ],
           "msg": "ensure this value has at least 1 characters",
           "type": "value_error.any_str.min_length",
           "ctx": {
             "limit_value": 1
           }
         }
       ]
    }


def test_create_user():
    body = {"first_name": "First Name",
            "last_name": "Last Name",
            "email": "first.name@mail.com",
            "gender": "N/A",
            "company": "None",
            "city": "Москва, Росси́йская Федера́ция",
            "title": "string",
            "id": str(uuid4())}

    response = client.post('/customers/', json=body)
    assert response.status_code == 201

    response = client.post('/customers/', json=body)
    assert response.status_code == 403
    assert response.json() == {f'detail':
                               f'Customer {body["id"]} already exists'}

    customer = body.copy()
    customer.pop('id')
    customer.update({"latitude": 55.751634,
                     "longitude": 37.618704})

    response = client.get(f'/customers/{body["id"]}')

    assert response.status_code == 200
    assert response.json() == customer
