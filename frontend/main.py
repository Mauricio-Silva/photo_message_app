# cSpell:disable
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import requests
from PIL import Image
import io


HEADERS = {"Content-Type": "application/json"}
MY_KEY = ""
BASE_URL = ""


class MainPage(BoxLayout):


    def start_new_conversation(self):
        global MY_KEY, BASE_URL
        BASE_URL = self.ids["url"].text
        request = requests.get(f"http://{BASE_URL}/new-key", headers=HEADERS)
        assert request.status_code == 200
        MY_KEY = dict(request.json()).get("key")
        print(MY_KEY)


    def enter_into_conversation(self):
        global MY_KEY, BASE_URL
        key = self.ids["user2_key"].text
        request = requests.get(f"http://{BASE_URL}/connect-key/{key}", headers=HEADERS)
        assert request.status_code == 200
        MY_KEY = dict(request.json()).get("key")


    def send_image(self):
        global MY_KEY
        print(MY_KEY)
        camera = self.ids['camera']
        camera.export_to_png(f"images/{MY_KEY}.jpg")
        data = {"key": MY_KEY}
        with open(f"images/{MY_KEY}.jpg","rb") as file:
            image = file.read()
        files = {"image": image}
        request = requests.post(f"http://{BASE_URL}/send-image", data=data, files=files)
        assert request.status_code == 200


    def get_image(self):
        global MY_KEY
        request = requests.get(f"http://{BASE_URL}/connect-key/{MY_KEY}", headers=HEADERS)
        assert request.status_code == 200
        image = Image.open(io.BytesIO(request.content))
        image.save(f"images/{MY_KEY}.jpg")
        self.ids["async_image"].source = f"images/{MY_KEY}.jpg"


        
        



class MainApp(App):
    def build(self):
        return MainPage()



MainApp().run()











