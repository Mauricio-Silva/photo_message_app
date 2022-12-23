# cSpell:disable
from android.permissions import request_permissions, Permission
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.app import App
from PIL import Image
import requests
import io
import os
Window.softinput_mode = 'below_target'


HEADERS = {"Content-Type": "application/json"}
BASE_PATH = "/sdcard/DCIM/PhotoMessenger"
# BASE_PATH = "images"


class StartScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class ChatScreen(Screen):
    pass

class PhotoScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

       

class MainApp(App):

    def build(self):
        global BASE_PATH
        if not os.path.exists(BASE_PATH):
            os.mkdir(BASE_PATH)
        self.title = "Photo Messenger"
        self.screen_managment = ScreenManager()
        self.screens = [
            StartScreen(name="start"), 
            LoginScreen(name="login"),
            ChatScreen(name="chat"),
            PhotoScreen(name="photo"),
            CameraScreen(name="camera"), 
        ]
        for screen in self.screens:
            self.screen_managment.add_widget(screen)
        self.screen_managment.current = "start"
        return self.screen_managment

    def run(self):
        request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        return super().run()

    def go_to_login(self):
        global BASE_URL
        BASE_URL = self.screen_managment.get_screen("start").ids["ip"].text
        BASE_URL = f"{BASE_URL}:9700"
        if len(BASE_URL) > 0 and not BASE_URL.isspace():
            self.screen_managment.switch_to(self.screens[1], direction="left")


    def back_to_start(self):
        self.screen_managment.switch_to(self.screens[0], direction="right")


    def start_new_conversation(self):
        global USERNAME, BASE_URL
        request = requests.get(f"http://{BASE_URL}/get-username1", headers=HEADERS)
        if request.status_code != 200:
            return None
        USERNAME = dict(request.json()).get("username")
        print(f"Username: {USERNAME}")
        self.screen_managment.switch_to(self.screens[2], direction="left")
        self.screen_managment.get_screen("chat").ids["my_pin"].text = USERNAME[6:]

    
    def enter_into_conversation(self):
        global USERNAME, BASE_URL
        pin: str = self.screen_managment.get_screen("login").ids["pin"].text
        pin = pin.upper()
        if len(pin) == 0 or pin.isspace():
            return None
        request = requests.get(f"http://{BASE_URL}/get-username2/{pin}", headers=HEADERS)
        if request.status_code != 200:
            return None
        USERNAME = dict(request.json()).get("username")
        print(f"Username: {USERNAME}")
        self.screen_managment.switch_to(self.screens[2], direction="left")
        self.screen_managment.get_screen("chat").ids["my_pin"].text = USERNAME[6:]


    def back_to_login(self):
        self.screen_managment.switch_to(self.screens[1], direction="right")


    def go_to_camera(self):
        self.screen_managment.switch_to(self.screens[4], direction="left")


    def get_image(self):
        global USERNAME, BASE_URL
        request = requests.get(f"http://{BASE_URL}/get-image/{USERNAME}", headers=HEADERS)
        if request.status_code != 200:
            return None
        image = Image.open(io.BytesIO(request.content))
        image.save(f"{BASE_PATH}/user2.jpg")
        self.screen_managment.get_screen("chat").ids["other_user_image"].reload()
        self.screen_managment.get_screen("chat").ids["other_user_image"].source = f"{BASE_PATH}/user2.jpg"


    def back_to_chat(self):
        self.screen_managment.switch_to(self.screens[2], direction="right")


    def take_picture(self):
        global USERNAME, BASE_PATH
        camera = self.screen_managment.get_screen("camera").ids["camera"]
        image_filepath = f"{BASE_PATH}/user1.jpg"
        camera.export_to_png(image_filepath)
        self.screen_managment.switch_to(self.screens[3], direction="right")
        self.screen_managment.get_screen("photo").ids["photo"].reload()
        self.screen_managment.get_screen("photo").ids["photo"].source = image_filepath


    def send_image(self):
        global USERNAME, BASE_PATH
        image_filepath = f"{BASE_PATH}/user1.jpg"
        data = {"username": USERNAME}
        with open(image_filepath, "rb") as file:
            image = file.read()
        files = {"image": image}
        request = requests.post(f"http://{BASE_URL}/send-image", data=data, files=files)
        if request.status_code != 200:
            return None
        self.screen_managment.switch_to(self.screens[2], direction="right")



MainApp().run()











