from werkzeug.datastructures import FileStorage
from PIL import Image
import uuid
import io



class Services:
    PATH = "app/static"


    @staticmethod
    def get_username1() -> str:
        return f"user1@{str(uuid.uuid4()).upper()[0:5]}"


    @staticmethod
    def get_username2(pin: str) -> str:
        return f"user2@{pin}"


    @classmethod
    def save_image(cls, username: str, buffer_image: FileStorage) -> None:
        image = Image.open(io.BytesIO(buffer_image.stream.read()))
        image.save(f"{cls.PATH}/{username}.jpg")


    @classmethod
    def get_username(cls, username: str) -> str:
        index = username.find("@") - 1
        number = username[index:index+1]
        if number == "1": 
            return f"user2@{username[index+2:]}"
        return f"user1@{username[index+2:]}"
        

    @classmethod
    def get_image_path(cls, username: str) -> str:
        pair_username = cls.get_username(username)
        return f"static/{pair_username}.jpg"
    


