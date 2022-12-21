from PIL import Image
import requests
import pytest
import io


GET_HEADERS = {"Content-Type": "application/json"}
# BASE_URL = "http://10.8.38.232:9700"
BASE_URL = "http://172.30.30.107:9700"
DATA = {
    "user1-key": "",
    "user2-key": "",
}

def get_request(suffix: str):
    return requests.get(f"{BASE_URL}/{suffix}", headers=GET_HEADERS)



def test_generate_new_key():
    global DATA
    request = get_request("new-key")
    key1 = dict(request.json()).get("key")
    assert request.status_code == 200
    assert key1 != None
    assert isinstance(key1, str)
    assert len(key1) == 5
    DATA["user1-key"] = key1


def test_connect_key():
    global DATA
    key1 = DATA["user1-key"]
    request = get_request(f"connect-key/{key1}")
    key2 = dict(request.json()).get("key")
    assert request.status_code == 200
    assert key2 != None
    assert isinstance(key2, str)
    assert len(key2) == 5
    DATA["user2-key"] = key2


def test_check_connection():
    global DATA
    key1 = DATA["user1-key"]
    key2 = DATA["user2-key"]
    request = get_request(f"check-connection/{key1}")
    connection = dict(request.json()).get("connection")
    assert request.status_code == 200
    assert connection != None
    assert isinstance(connection, bool)
    request = get_request(f"check-connection/{key2}")
    connection = dict(request.json()).get("connection")
    assert request.status_code == 200
    assert connection != None
    assert isinstance(connection, bool)


def test_send_image():
    global DATA
    key1 = DATA["user1-key"]
    data = {"key": key1}
    with open("tests/city.jpeg","rb") as file:
        image = file.read()
    files = {"image": image}
    request = requests.post(f"{BASE_URL}/send-image", data=data, files=files)
    assert request.status_code == 200


def test_get_image():
    global DATA
    key2 = DATA["user2-key"]
    request = get_request(f"get-image/{key2}")
    assert len(request.content) > 0
    assert request.status_code == 200
    try:
        Image.open(io.BytesIO(request.content))
    except Exception as exc:
        pytest.fail(exc, pytrace=True)


def test_check_image():
    global DATA
    key2 = DATA["user2-key"]
    request = get_request(f"check-image/{key2}")
    assert request.status_code == 200
    assert not dict(request.json()).get("change")

