import os
from select import select

from starlette.testclient import TestClient

from app.main import app
from database.models import Item

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Fast API in Python'}


def test_insert_item(db_session_fixture):
    response = client.post('/items/', json={"name": "item1"})
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {"name": "item1"}

    # Now check the database to confirm that the item was actually inserted
    item_id = response.json().get("id")  # Extract the id from the response

    # Query the database to ensure the item exists
    item = db_session_fixture.exec(select(Item).where(Item.id == item_id)).first()

    # Check if the item is present in the database
    assert item is not None

    # Check if the item name matches the one we inserted
    assert item.name == "item1"

# def test_get_item(db_session):
#     post_response = client.post('/items/', json={"name": "item1"})
#     get_response = client.get('/items/item1')
#     assert get_response.status_code == 200
#     assert get_response.json() == {"name": "item1"}
#
#
# def test_insert_item_audit_log(db_session):
#     response = client.post('/items/', json={"name": "item1"})
#     assert response.status_code == 201
#     assert response.json() == {"name": "item1"}
#     audit_log = client.get('/audit_log/')
#     assert audit_log.status_code == 200
#     assert audit_log.json() == [{"table_name": "item", "record_id": 1, "user_id": None, "action": "INSERT",
#                                  "new_value": "{'name': 'item1'}"}]
