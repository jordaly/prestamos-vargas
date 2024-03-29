import json
import ttkbootstrap as tkb
from ttkbootstrap import constants
from pathlib import Path
from datetime import datetime
from enum import Enum
from settings import DATA_PATH


class tkinter_events(Enum):
    BUTTON = "<Button>"  # One mouse button is pressed
    buttonRelease = "<ButtonRelease>"  # One mouse button is released
    CONFIGURE = "<Configure>"  # The size or location of the widget changes
    ACTIVATE = (
        "<Activate>"  # The state option of a widget changes from inactive to active.
    )
    DEACTIVATE = (
        "<Deactivate>"  # The state option of a widget changes from active to inactive
    )
    DESTROY = "<Destroy>"  # The widget is destroyed
    ENTER = "<Enter>"  # The mouse pointer is moved into a visible part of a widget.
    LEAVE = "<Leave>"  # The mouse pointer is moved out of a visible part of a widget.
    EXPOSE = "<Expose>"  # Some part of the widget or application is visible after having been covered up by another window.
    FOCUSIN = "<FocusIn>"  # The input focus was moved into a widget.
    FOCUSOUT = "<FocusOut>"  # The input focus was moved from a widget.
    KEYPRESS = "<KeyPress>"  # A key is pressed
    KEYRELEASE = "<KeyRelease>"  # A key is released
    MAP = "<Map>"  # A widget is being placed on a container e.g., calling the pack() or grid() method.
    UNMAP = "<Unmap>"  # A widget is being unmapped and is no longer visible, for example when calling the grid_remove() method on the widget.
    MOTION = "<Motion>"  # The mouse pointer is moved entirely within a widget.
    MOUSEWHEEL = "<MouseWheel>"  # The mouse wheel is rotated
    VISIBILITY = "<Visibility>"  # At least some part of the application window becomes visible on the screen.


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
    def __init__(self, trigger: str, code: event_types, data: dict[any] = None):
        self.trigger = trigger
        self.code = code.value
        self.data = data if data else {}

    def __str__(self):
        return f"event: ({self.name}) from ({self.trigger})"

    def handle(self, app: tkb.Window):
        match self.code:
            case event_types.LOGIN.value:
                print("handling event")
                app.user_auth = self.data["user"]
                app.last_user_login = self.data["user"]["username"]

                app.menu.user = app.user_auth
                app.menu.username_lb_var.set(app.user_auth["username"])

                self.change_current_frame(
                    app=app,
                    new_frame=app.menu,
                    expand=True,
                    fill=constants.BOTH,
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
                    fill=constants.BOTH,
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
            for widget in app.menu.content.winfo_children():
                widget.forget()
            app.menu.content = new_frame
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
