from base import client


def test_category_full():

    # create
    name = "test"
    data = {
        "name": name,
        "is_active": True
    }
    response = client.post("/category/create/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == name
    # end create
    category_id = response.json()["id"]

    # create
    name = "test subcategory"
    data = {
        "name": name,
        "is_active": True,
        'category_id': category_id
    }
    response = client.post("/subcategory/create/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == name
    # end create
    subcategory_id = response.json()["id"]

    # detail
    response = client.get(f"/subcategory/detail/{subcategory_id}/")
    assert response.status_code == 200
    assert response.json()["name"] == name

    name = "new_name"
    data = {
        "name": name,
        "is_active": True,
        'category_id': category_id
    }
    # end detail

    # update
    response = client.put(f"/subcategory/update/{subcategory_id}/", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == name
    # end  update

    # delete
    response = client.delete(f"/subcategory/delete/{subcategory_id}/")
    assert response.status_code == 200

    # delete
    response = client.delete(f"/category/delete/{category_id}/")
    assert response.status_code == 200

    # detail for 404
    response = client.get(f"/subcategory/detail/{subcategory_id}/")
    assert response.status_code == 404
