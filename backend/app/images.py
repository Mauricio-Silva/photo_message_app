from werkzeug.datastructures import FileStorage
from PIL import Image
from app.keys import Keys
import os
import io


class Images:
    PATH = "app/static"
    CHANGES = {}


    @classmethod
    def init(cls) -> None:
        if not os.path.exists(cls.PATH):
            os.mkdir(cls.PATH)


    @classmethod
    def save_image(cls, user_key: str, buffer_image: FileStorage) -> None:
        image = Image.open(io.BytesIO(buffer_image.stream.read()))
        image.save(f"{cls.PATH}/{user_key}.jpg")
        cls.CHANGES[user_key] = True


    @classmethod
    def get_image(cls, user_key: str) -> str:
        key = Keys.get_key(user_key)
        cls.CHANGES[key] = False
        return f"static/{key}.jpg"
    
    
    @classmethod
    def check_change(cls, user_key: str) -> bool:
        key = Keys.get_key(user_key)
        return cls.CHANGES[key]




