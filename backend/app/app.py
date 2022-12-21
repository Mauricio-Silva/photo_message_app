from flask import Flask, request, Response, send_file
from app.images import Images
from app.keys import Keys
import json


app = Flask(__name__)
TYPE = "application/json"


def get_response(data: dict = None, code: int = 200) -> Response:
    HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True, "Content-Type": TYPE}
    if data is None:
        return Response(None, code, HEADERS, mimetype=TYPE)
    return Response(json.dumps(data, indent=2), code, HEADERS, mimetype=TYPE)



@app.route("/new-key", methods=["GET"])
def generate_new_key():
    if request.method == "GET":
        key = Keys.generate()
        Keys.register_user1(key)
        return get_response({"key": key})      



@app.route("/connect-key/<key>", methods=["GET"])
def connect_key(key: str):
    if request.method == "GET":
        pair_key = Keys.generate()
        Keys.register_user2(key, pair_key)
        return get_response({"key": pair_key})
      


@app.route("/check-connection/<key>", methods=["GET"])
def check_connection(key: str):
    if request.method == "GET":
        if Keys.check_connection(key):
            return get_response({"connection": True})
        return get_response({"connection": False})



@app.route("/list", methods=["GET"])
def list():
    if request.method == "GET":
        return get_response(Keys.find_all())



@app.route("/send-image", methods=["POST"])
def send_image():
    if request.method == "POST":
        key = request.form.get("key")
        buffer_file = request.files['image']
        Images.save_image(key, buffer_file)
        return get_response()



@app.route("/get-image/<key>", methods=["GET"])
def get_image(key: str):
    if request.method == "GET":
        image_path = Images.get_image(key)
        return send_file(image_path, "image/jpg")



@app.route("/check-image/<key>", methods=["GET"])
def check_image(key: str):
    if request.method == "GET":
        if Images.check_change(key):
            return get_response({"change": True})
        return get_response({"change": False})
