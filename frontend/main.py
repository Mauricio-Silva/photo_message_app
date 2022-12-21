# cSpell:disable
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
from PIL import Image
import io


HEADERS = {"Content-Type": "application/json"}
MY_KEY = ""
BASE_URL = ""


class StartScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

class ChatScreen(Screen):
    pass

       

class MainApp(App):
    def build(self):
        # self.file = Builder.load_file("main.kv")
        self.screen_managment = ScreenManager()
        self.screens = [StartScreen(name="main-page"), CameraScreen(name="camera"), ChatScreen(name="chat0xx")]
        self.screen_managment.add_widget(self.screens[0])
        self.screen_managment.add_widget(self.screens[1])
        self.screen_managment.add_widget(self.screens[2])
        self.screen_managment.current = "main-page"
        return self.screen_managment


    # sm.switch_to(screens[1], direction='right')



    def start_new_conversation(self):
        # global MY_KEY, BASE_URL
        # BASE_URL = self.ids["url"].text
        # request = requests.get(f"http://{BASE_URL}/new-key", headers=HEADERS)
        # assert request.status_code == 200
        # MY_KEY = dict(request.json()).get("key")
        # print(f"Key: {MY_KEY}")
        self.screen_managment.switch_to(self.screens[2], direction="left")

    
    def enter_into_conversation(self):
        # global MY_KEY, BASE_URL
        # key = self.ids["user2_key"].text
        # request = requests.get(f"http://{BASE_URL}/connect-key/{key}", headers=HEADERS)
        # assert request.status_code == 200
        # MY_KEY = dict(request.json()).get("key")
        self.screen_managment.switch_to(self.screens[2], direction="left")


    def back_to_start(self):
        self.screen_managment.switch_to(self.screens[0], direction="right")


    def get_image(self):
        global MY_KEY
        request = requests.get(f"http://{BASE_URL}/connect-key/{MY_KEY}", headers=HEADERS)
        assert request.status_code == 200
        image = Image.open(io.BytesIO(request.content))
        image.save(f"images/{MY_KEY}.jpg")
        self.ids["async_image"].source = f"images/{MY_KEY}.jpg"


    def take_picture(self):
        self.screen_managment.switch_to(self.screens[1], direction="left")


    def send_image(self):
        # global MY_KEY

        camera = self.screen_managment.get_screen("camera").ids["camera"]
        # camera = self.get_screen("camera").ids['camera']

        # camera.export_to_png(f"images/{MY_KEY}.jpg")
        camera.export_to_png(f"images/001.jpg")
        # data = {"key": MY_KEY}
        # with open(f"images/{MY_KEY}.jpg","rb") as file:
        #     image = file.read()
        # files = {"image": image}
        # request = requests.post(f"http://{BASE_URL}/send-image", data=data, files=files)
        # assert request.status_code == 200

        self.screen_managment.get_screen("camera")
        # self.screen_managment.get_screen("chat").ids["async_image"].source = f"images/001.jpg"
        self.screen_managment.switch_to(self.screens[2], direction="right")




MainApp().run()











