from PIL import Image
import requests
import pytest
import io


GET_HEADERS = {"Content-Type": "application/json"}
BASE_URL = "http://172.30.30.107:9700"
DATA = {
    "username1": "",
    "username2": "",
}

def get_request(suffix: str):
    return requests.get(f"{BASE_URL}/{suffix}", headers=GET_HEADERS)



def test_get_username1():
    global DATA
    request = get_request("get-username1")
    username = dict(request.json()).get("username")
    assert request.status_code == 200
    assert username != None
    DATA["username1"] = username


def test_get_username2():
    global DATA
    username1 = DATA["username1"]
    request = get_request(f"get-username2/{username1}")
    username2 = dict(request.json()).get("username")
    assert request.status_code == 200
    assert username2 != None
    DATA["username2"] = username2


def test_send_image():
    global DATA
    username1 = DATA["username1"]
    data = {"username": username1}
    with open("tests/city.jpeg","rb") as file:
        image = file.read()
    files = {"image": image}
    request = requests.post(f"{BASE_URL}/send-image", data=data, files=files)
    assert request.status_code == 200


def test_get_image():
    global DATA
    username2 = DATA["username2"]
    request = get_request(f"get-image/{username2}")
    assert len(request.content) > 0
    assert request.status_code == 200
    try:
        Image.open(io.BytesIO(request.content))
    except Exception as exc:
        pytest.fail(exc, pytrace=True)


