import ttkbootstrap as tkb
from ttkbootstrap import constants
from tkinter import messagebox
from events import Event, event_types
from settings import ASSETS_PATH
from User import views as user_views


class Menu(tkb.Frame):
    def __init__(self, parent, listen_event: callable):
        super().__init__(parent)
        self.parent = parent
        self.listen_event = listen_event

        self.bind("<Configure>", lambda e: self.resize_content(e))
        self.configure_grid()

        self.load_topbar()
        self.load_sidebar()
        self.load_content()
        self.load_navigation()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=3)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=7)

    # topbar should have a photo of the system and the name of the user in the other side (photo of the left and name of the right)
    def load_topbar(self):
        self.topbar_frame = tkb.Frame(self, bootstyle=constants.DARK)
        self.topbar_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.logo_img = tkb.Image.open(ASSETS_PATH / "img" / "logo.png").resize(
            (40, 30)
        )
        self.logo_imgtk = tkb.ImageTk.PhotoImage(self.logo_img)

        self.logo_lb = tkb.Label(self.topbar_frame, image=self.logo_imgtk)
        self.logo_lb.pack(side="left", padx=10)

        self.name_lb_var = tkb.StringVar(value="User Name")
        self.name_lb = tkb.Label(
            self.topbar_frame,
            textvariable=self.name_lb_var,
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.name_lb.pack(side="right", padx=10)

    def load_sidebar(self):
        self.sidevar = tkb.Frame(self, bootstyle=constants.SECONDARY)
        self.sidevar.grid(column=0, row=1, sticky="nsew")

        self.add_user_button = tkb.Button(
            self.sidevar,
            text="Add User",
            command=self.add_user,
            bootstyle=constants.DARK,
        )

        self.add_user_button.pack(pady=5, padx=5, fill="x")

        self.logout_btn = tkb.Button(
            self.sidevar, text="Logout", command=self.logout, bootstyle=constants.DARK
        )
        self.logout_btn.pack(pady=5, padx=5, fill="x")

    def load_content(self):
        self.content = tkb.Frame(self)
        self.content.grid(column=1, row=1, sticky="nsew")
        self.label = tkb.Label(self.content, text="Welcome to the Menu")
        self.label.pack()

    def load_navigation(self):
        self.user_panel_view = user_views.UsersPanel(self.content)
        self.user_form_view = user_views.UserForm(self.content)

    # Navigation methods
    def add_user(self):
        self.listen_event(
            Event(trigger=self._get_name(), code=event_types.ADD_USER, data={})
        )

    def resize_content(self, event):
        print(event)

        # <Configure event x=0 y=0 width=500 height=300> this are the default values of the event

        width = 500  # column
        height = 300  # row

        # and this are the default values of the frame rowconf and columnconf of the content
        def_x = 3  # column
        def_y = 7  # row

        # here we calculate the increment of the width and height of the content
        # this value will incremente in 1 for each interval of pixels of the event
        pixel_in_x = 30
        pixel_in_y = 35
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
