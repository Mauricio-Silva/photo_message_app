from PIL import Image
import requests
import io


GET_HEADERS = {"Content-Type": "application/json"}
BASE_URL = "http://172.30.30.107:9700"



def get_username2(username1: str):
    request = requests.get(f"{BASE_URL}/get-username2/{username1}")
    assert request.status_code == 200
    username2 = dict(request.json()).get("username")
    print(username2)


def send_image(username: str):
    data = {"username": username}
    with open("tests/city.jpeg","rb") as file:
        image = file.read()
    files = {"image": image}
    request = requests.post(f"{BASE_URL}/send-image", data=data, files=files)
    assert request.status_code == 200


def get_image(username: str):
    request = requests.get(f"{BASE_URL}/get-image/{username}")
    assert request.status_code == 200
    image = Image.open(io.BytesIO(request.content))
    image.show()






# get_username2("B7A6E")

# send_image("user2@525AE")

# get_image("user2@525AE")



