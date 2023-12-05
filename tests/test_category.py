from base import client


def test_category_create():
    # data = {
    #     "name": "test",
    #     "is_active": True
    # }
    # response = client.post("/category/create/", json=data)
    # assert response.status_code == 200

    response = client.get(f"/category/all/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
