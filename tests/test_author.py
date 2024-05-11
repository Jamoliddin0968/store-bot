from typing import List

from base import client


def test_author():

    # create
    name = "test"
    data = {
        "firstname": name,
        "lastname": "name",
        "birthdate": 1616489,
        "country": "str",
    }
    response = client.post("/author/create/", json=data)
    assert response.status_code == 200
    assert response.json()["firstname"] == name
    # end create

    author_id = response.json()["id"]
    # detail
    response = client.get(f"/author/detail/{author_id}/")
    assert response.status_code == 200
    # end detail

    # update
    response = client.put(f"/author/update/{author_id}/", json=data)
    assert response.status_code == 200
    assert response.json()["firstname"] == name
    # end  update

    # get all
    response = client.get("/author/all/")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    # end get all

    # delete
    response = client.delete(f"/author/delete/{author_id}/")
    assert response.status_code == 200
