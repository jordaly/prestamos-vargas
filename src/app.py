import json
import platform
import asyncio
import settings
import ttkbootstrap as tkb
from ttkbootstrap import font as tkfont, constants
from auth.login import Login
from menu.menu import Menu
from database.models import Session
from events import Event


class App(tkb.Window):
    session = Session()
    user_auth = None
    current_frame = None
    current_menu_content = None
    popup_windows = []
    current_path = settings.CURRENT_PATH
    assets_path = settings.ASSETS_PATH
    data_path = settings.DATA_PATH

    def __init__(self, title, size, icon_path):
        super().__init__(iconphoto=str(self.assets_path / icon_path))

        self.title(title)
        self.minsize(size[0], size[1])

        self.configure_styles()

        self.main_frame = tkb.Frame(self)
        self.main_frame.pack(expand=True, fill=constants.BOTH)

        self.current_platform = platform.system()

        if self.current_platform == "Linux":
            self.defaultFont = tkfont.Font(family="gothic", size=11)
            self.option_add("*Font", self.defaultFont)

        self.last_user_login = self.look_last_user()

        self.menu = Menu(self.main_frame, self.listen_event)
        self.login = Login(self.main_frame, self.listen_event, self.last_user_login)

        self.current_frame = self.login
        self.current_frame.pack(expand=True, fill=constants.BOTH, padx=20, pady=20)

    def configure_styles(self):
        pass

    def look_last_user(self):
        result = None
        try:
            with open(self.data_path, "r") as file:
                data = json.load(file)

            result = data["last_user_logged"]["username"]

        except Exception:
            print("there was an error while trying to read data.json")

        return result

    def listen_event(self, event: Event):
        event.handle(self)
        self.show_app_status()

    def show_app_status(self):
        username = None

        if self.user_auth:
            username = self.user_auth["username"]

        print(
            {
                "user_auth": username,
                "popup_windows": len(self.popup_windows),
                "current_frame": self.current_frame.__class__.__name__,
            }
        )

    async def mainloop_async(self):
        await self.show()

    async def show(self):
        interval = 0.1
        while True:
            self.update()
            try:
                self.state()
            except Exception:
                break
            await asyncio.sleep(interval)
