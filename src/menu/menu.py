import tkinter as tk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from tkinter import ttk
from tkinter import messagebox
from events import Event, event_types


class Menu(tkb.Frame):
    def __init__(self, parent, listen_event: callable):
        super().__init__(parent)
        self.parent = parent
        self.listen_event = listen_event

        self.bind("<Configure>", lambda e: self.resize_content(e))
        self.configure_grid()

        self.load_sidebar()
        self.load_content()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=3)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=5)

    def load_sidebar(self):
        self.sidevar = tkb.Frame(self, bootstyle=SECONDARY)
        self.sidevar.grid(column=0, row=1, sticky="nsew")

        self.add_user_button = tkb.Button(
            self.sidevar, text="Add User", command=self.add_user, bootstyle=DARK
        )
        self.add_user_button.pack(pady=5, padx=5, fill="x")

        self.logout_btn = tkb.Button(
            self.sidevar, text="Logout", command=self.logout, bootstyle=DARK
        )
        self.logout_btn.pack(pady=5, padx=5, fill="x")

    def load_content(self):
        self.content = tkb.Frame(self)
        self.content.grid(column=1, row=1, sticky="nsew")
        self.label = tkb.Label(self.content, text="Welcome to the Menu")
        self.label.pack()

    def add_user(self):
        pass

    def resize_content(self, event):
        print(event)

        # <Configure event x=0 y=0 width=500 height=300> this are the default values of the event

        width = 500  # column
        height = 300  # row

        # and this are the default values of the frame rowconf and columnconf of the content
        def_x = 3  # column
        def_y = 5  # row

        # here we calculate the increment of the width and height of the content
        # this value will incremente in 1 for each interval of pixels of the event
        pixel_in_x = 30
        pixel_in_y = 50
        increment_x = int((event.width - width) / pixel_in_x) + def_x
        increment_y = int((event.height - height) / pixel_in_y) + def_y

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=increment_x)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=increment_y)

    def logout(self):

        result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
        print(result)
        if result == "yes":
            self.listen_event(
                Event(trigger=self._get_name(), code=event_types.LOGOUT, data={})
            )

    @classmethod
    def _get_name(cls):
        return cls.__name__
