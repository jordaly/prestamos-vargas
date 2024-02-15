import ttkbootstrap as tkb
from ttkbootstrap import constants
from tkinter import messagebox
from events import Event, event_types
from settings import ASSETS_PATH


class Menu(tkb.Frame):
    user = None
    content_views = dict()

    def __init__(self, parent, listen_event: callable):
        super().__init__(parent)
        self.parent = parent
        self.listen_event = listen_event

        self.configure_grid()

        self.load_topbar()
        self.load_sidebar()
        self.load_content()

        self.load_navigation()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=0, minsize=100)
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=0, minsize=50)
        self.rowconfigure(index=1, weight=1)

    def load_topbar(self):
        style = tkb.Style.get_instance()
        style.configure("logoMain.TButton", padding=0, relief=constants.FLAT)

        self.topbar_frame = tkb.Frame(self, bootstyle=constants.DARK)
        self.topbar_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.logo_img = tkb.Image.open(ASSETS_PATH / "img" / "logo.png").resize(
            (40, 30)
        )

        self.logo_imgtk = tkb.ImageTk.PhotoImage(self.logo_img)

        self.logo_btn = tkb.Button(
            self.topbar_frame,
            command=self.load_welcome,
            image=self.logo_imgtk,
            bootstyle=constants.DARK,
            style="logoMain.DARK.TButton",
        )
        self.logo_btn.pack(side="left", padx=10)

        self.username_lb_var = tkb.StringVar(value="User Name")
        self.name_lb = tkb.Label(
            self.topbar_frame,
            textvariable=self.username_lb_var,
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.name_lb.pack(side="right", padx=10)

    def load_sidebar(self):
        self.sidevar = tkb.Frame(self, bootstyle=constants.SECONDARY)
        self.sidevar.grid(column=0, row=1, sticky="nsew")

        self.add_user_button = tkb.Button(
            self.sidevar,
            text="Add User",
            command=self.load_user_panel,
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
        from User import views as user_views

        self.content_views = {
            "user": user_views.UserView(self.content),
        }

    def load_welcome(self):
        self.clean_content()
        tkb.Label(self.content, text="Welcome to the Menu").pack()

    def clean_content(self):
        for view in self.content.winfo_children():
            view.forget()

    # Navigation methods
    def load_user_panel(self):
        self.clean_content()

        self.content_views["user"].pack(expand=True, fill="both")

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
