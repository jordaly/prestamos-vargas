import json
import platform
import tkinter as tk
import tkinter.font as tkfont
import ttkbootstrap as tkb
from auth.login import Login
from menu.menu import Menu
from events import Event
from database.db import Session
import settings


class App(tkb.Window):
    session = Session()
    user_auth = None
    current_frame = None
    popup_windows = []
    current_path = settings.CURRENT_PATH
    assets_path = settings.ASSETS_PATH
    data_path = settings.DATA_PATH

    def __init__(self, title, size, icon_path):
        super().__init__()

        self.iconphoto(
            True, tkb.ImageTk.PhotoImage(tkb.Image.open(self.assets_path / icon_path))
        )

        self.title(title)
        self.minsize(size[0], size[1])

        self.main_frame = tkb.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # print(tkfont.families())
        self.current_platform = platform.system()
        if self.current_platform == "Linux":
            self.defaultFont = tkfont.Font(family="gothic", size=11)
            self.option_add("*Font", self.defaultFont)

        # self.defaultfont = tkfont.nametofont()

        self.last_user_login = self.look_last_user()

        self.menu = Menu(self.main_frame, self.listen_event)
        self.login = Login(self.main_frame, self.listen_event, self.last_user_login)

        self.current_frame = self.login
        self.current_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

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
