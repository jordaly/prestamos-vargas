import json
import tkinter as tk
import ttkbootstrap as tkb
from pathlib import Path
from datetime import datetime
from enum import Enum
from settings import DATA_PATH


class event_types(Enum):
    LOGIN = 1
    LOGIN_FAILED = 2
    LOGOUT = 3
    ADD_USER = 4
    ADD_CLIENT = 5
    ADD_LOAN = 6
    ADD_PAYMENT = 7
    GO_TO_MAIN = 8


class Event:
    from app import App

    def __init__(self, trigger: str, code: event_types, data: dict[any] = None):
        self.trigger = trigger
        self.code = code.value
        self.data = data if data else {}

    def __str__(self):
        return f"event: ({self.name}) from ({self.trigger})"

    def handle(self, app: App):
        match self.code:
            case event_types.LOGIN.value:
                print("handling event")
                app.user_auth = self.data["user"]
                app.last_user_login = self.data["user"]["username"]
                self.change_current_frame(
                    app=app,
                    new_frame=app.menu,
                    expand=True,
                    fill=tk.BOTH,
                )
                self.modify_app_log(DATA_PATH, user=self.data["user"])

            case event_types.LOGIN_FAILED.value:
                print("login failed")

            case event_types.LOGOUT.value:
                print("logout")
                app.user_auth = None
                self.change_current_frame(
                    app=app,
                    new_frame=app.login,
                    expand=True,
                    fill=tk.BOTH,
                    padx=20,
                    pady=20,
                )

            case event_types.ADD_USER.value:
                print("add user")
                # self.change_current_frame(app=)

            case event_types.ADD_CLIENT.value:
                print("add client")

            case event_types.ADD_LOAN.value:
                print("add loan")

            case event_types.ADD_PAYMENT.value:
                print("add payment")

            case event_types.GO_TO_MAIN.value:
                print("go to main")
            case _:
                print("no event")

    def change_current_frame(
        self,
        app: tkb.Window,
        new_frame: tkb.Frame | tkb.LabelFrame,
        menu=False,
        **kwargs,
    ) -> None:
        if menu:
            app.menu.content.forget()
            app.menu.content = app.menu.user_panel_view
            app.menu.content.pack(**kwargs)
            return
        app.current_frame.forget()
        app.current_frame = new_frame
        app.current_frame.pack(**kwargs)

    def modify_app_log(self, path: Path | str, user: dict[any]):
        data = {}
        current_date = datetime.now().timestamp()

        try:
            with open(path, "r+") as file:
                file.seek(0)
                result = file.read()
                current_date = datetime.now().timestamp()

                if not result:
                    data = {
                        "last_user_logged": {
                            "id": user["id"],
                            "username": user["username"],
                            "email": user["email"],
                        },
                        "login_history": [
                            {
                                "id": user["id"],
                                "username": user["username"],
                                "date": current_date,
                            }
                        ],
                        "created_at": current_date,
                        "updated_at": current_date,
                    }

                    file.seek(0)
                    file.write(json.dumps(data, indent=2))
                    file.truncate()

                data = json.loads(result)

                data["last_user_logged"] = {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                }

                login_history = data["login_history"]

                if len(login_history) >= 10:
                    login_history.pop(0)

                login_history.append(
                    {
                        "id": user["id"],
                        "username": user["username"],
                        "date": current_date,
                    }
                )

                data["login_history"] = login_history
                data["updated_at"] = current_date

                file.seek(0)
                file.write(json.dumps(data, indent=2))
                file.truncate()

        except OSError:
            with open(path, "w") as file:
                data = {
                    "last_user_logged": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"],
                    },
                    "login_history": [
                        {
                            "id": user["id"],
                            "username": user["username"],
                            "date": current_date,
                        }
                    ],
                    "created_at": current_date,
                    "updated_at": current_date,
                }
                file.write(json.dumps(data, indent=2))

        return data["last_user_logged"]["username"]
