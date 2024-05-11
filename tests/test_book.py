from base import client


def test_create_book():
    book_data = {
        "name": "Test Book",
        "description": "Test Description",
        "author_id": 1,
        "subcategory_id": 1,
        "file": "test.pdf",
        "audio_file": "test.mp3"
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Book"
    assert response.json()["description"] == "Test Description"


def test_read_book():
    # Assuming book_id is 1 for the test book created in test_create_book
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Book"
    assert response.json()["description"] == "Test Description"


def test_update_book():
    book_update_data = {
        "name": "Updated Book",
        "description": "Updated Description",
        "author_id": 2,
        "subcategory_id": 2,
        "file": "updated_test.pdf",
        "audio_file": "updated_test.mp3"
    }
    response = client.put("/books/1", json=book_update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Book"
    assert response.json()["description"] == "Updated Description"


def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    # Assuming we return the deleted object
    assert response.json()["name"] == "Updated Book"
    # Assuming we return the deleted object
    assert response.json()["description"] == "Updated Description"
