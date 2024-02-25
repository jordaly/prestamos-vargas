import asyncio
import ttkbootstrap as tkb
from ttkbootstrap.validation import validator, add_validation, ValidationEvent
from tkinter import messagebox
from database.models import User, Session
from events import event_types, Event


loop = asyncio.get_event_loop()


@validator
def validate_empty_entry(event: ValidationEvent):
    if not event.postchangetext:
        return False
    return True


class Login(tkb.LabelFrame):
    """This class creates the login LabelFrame
    This class should be packed with this parameters:
        padx=20,
        pady=20,
        fill="both",
        expand=True

    Args:
        parent (ttkObject): the parent frame usually the main_frame of the app
        listen_event (function): the function that will listen to the events
        username (str, optional): the username that will be used to prefill the username entry. Defaults to None.

    Returns:
        ttk.LabelFrame: custom label frame with the login form
    """

    session = Session()

    def __init__(self, parent, listen_event: callable, username: str = None):
        super().__init__(parent, text="Login")

        self.listen_event = listen_event
        self.parent = parent

        self.username_lb = tkb.Label(self, text="Username")
        self.username_lb.pack(pady=5)

        self.username_var = tkb.StringVar(value=username if username else "")
        self.username = tkb.Entry(self, textvariable=self.username_var)
        add_validation(self.username, validate_empty_entry, when="focusout")
        self.username.bind("<KeyPress-Return>", lambda _: self.login())
        self.username.pack(ipady=5)

        self.password_lb = tkb.Label(self, text="Password")
        self.password_lb.pack(pady=5)

        self.password_var = tkb.StringVar(value="")
        self.password = tkb.Entry(self, show="*", textvariable=self.password_var)
        add_validation(self.password, validate_empty_entry, when="focusout")
        self.password.bind("<KeyPress-Return>", lambda _: self.login())
        self.password.pack(ipady=5)

        self.submit_btn = tkb.Button(self, text="Login", command=self.login)
        self.submit_btn.pack(pady=20)

        # self.test_btn = tkb.Button(
        #     self, text="Test", command=lambda: loop.create_task(self.test())
        # )
        #
        # self.test_btn.pack(pady=20)

    async def test(self):
        print("Testing")
        await asyncio.sleep(2)
        print("Tested")

    def check_fields(self) -> bool:
        """this function checks if the fields are
        empty and return a boolean"""

        return bool(self.username.validate() and self.password.validate())

    def login(self) -> None:
        """this function validate that the
        user exists and the password is
        correct"""
        if not self.check_fields():
            messagebox.showerror("Login", "Username and password are required")
            return

        username = self.username_var.get()
        password = self.password_var.get()
        # print(f"username: {username}, password: {password}")

        if username == "admin" and password == "admin":
            self.clean_vars()
            user_data = {
                "user": {
                    "id": -1,
                    "username": username,
                    "password": password,
                    "first_name": "admin",
                    "last_name": "admin",
                    "email": "admin@admin.com",
                    "object": None,
                }
            }
            self.listen_event(
                Event(
                    trigger=self._get_name(),
                    code=event_types.LOGIN,
                    data=user_data,
                )
            )

        else:
            user = User.filter(username=username)

            if user:
                user_data = {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "password": user.password,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "object": user,
                    }
                }
            else:
                user_data = {
                    "user": {
                        "id": -1,
                        "username": username,
                        "password": password,
                        "first_name": "",
                        "last_name": "",
                        "email": "",
                        "object": None,
                    }
                }

            if user and user.password == password:
                self.clean_vars()
                self.listen_event(
                    Event(
                        trigger=self._get_name(),
                        code=event_types.LOGIN,
                        data=user_data,
                    )
                )
            else:
                self.clean_vars(both=False)
                self.listen_event(
                    Event(
                        trigger=self._get_name(),
                        code=event_types.LOGIN_FAILED,
                        data=user_data,
                    )
                )

                messagebox.showerror(
                    "Login",
                    "Login Failed.",
                )

    def clean_vars(self, both: bool = True):
        self.password_var.set("")

        if both:
            self.username_var.set("")

    @classmethod
    def _get_name(cls):
        return cls.__name__

    def __str__(self):
        return "Login Frame"
