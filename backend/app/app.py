from flask import Flask, request, Response, send_file
from app.services import Services
import json


app = Flask(__name__)
TYPE = "application/json"


def get_response(data: dict = None, code: int = 200) -> Response:
    HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Content-Type": TYPE}
    if data is None:
        return Response(None, code, HEADERS, mimetype=TYPE)
    return Response(json.dumps(data, indent=2), code, HEADERS, mimetype=TYPE)



@app.route("/get-username1", methods=["GET"])
def get_username1():
    if request.method == "GET":
        username = Services.get_username1()
        return get_response({"username": username})      



@app.route("/get-username2/<pin>", methods=["GET"])
def get_username2(pin: str):
    if request.method == "GET":
        pair_username = Services.get_username2(pin)
        return get_response({"username": pair_username})



@app.route("/send-image", methods=["POST"])
def send_image():
    if request.method == "POST":
        username = request.form.get("username")
        buffer_file = request.files["image"]
        Services.save_image(username, buffer_file)
        return get_response()



@app.route("/get-image/<username>", methods=["GET"])
def get_image(username: str):
    if request.method == "GET":
        image_path = Services.get_image_path(username)
        return send_file(image_path, "image/jpg")


