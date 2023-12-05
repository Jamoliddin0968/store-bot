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
    response = client.delete(f"/author/delete/{author_id}/")
    assert response.status_code == 200
