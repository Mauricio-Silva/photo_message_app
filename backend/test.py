from PIL import Image
import requests
import json
import io



def get_key(key: str):
    request = requests.get(f"http://10.8.38.245:9700/connect-key/{key}")
    key1 = dict(request.json()).get("key")
    print(key1)


def send_image(key: str):
    data = {"key": key}
    with open("tests/city.jpeg","rb") as file:
        image = file.read()
    files = {"image": image}
    request = requests.post(f"http://10.8.38.245:9700/send-image", data=data, files=files)
    assert request.status_code == 200


def get_image(key: str):
    request = requests.get(f"http://10.8.38.245:9700/get-image/{key}")
    assert request.status_code == 200
    image = Image.open(io.BytesIO(request.content))
    image.show()



# get_key("")

# send_image("")

# get_image("")



text = "user1@abcdef"
index = text.find("@") - 1
print(text[index:index+1])
print(text[index+2:])