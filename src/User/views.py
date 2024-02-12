import ttkbootstrap as tkb
from ttkbootstrap import constants


class UsersPanel(tkb.Frame):
    topbar_bg_color = "#CCC"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure_grid()

        self.load_topbar()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=8)

    def load_topbar(self):
        self.topbar_frame = tkb.Frame(self, background=self.topbar_bg_color)
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame,
            text="Users Panel",
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.title_lb.pack(side="left", padx=10)


class UserForm(tkb.Frame):
    topbar_bg_color = "#CCC"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure_grid()

        self.load_topbar()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=8)

    def load_topbar(self):
        self.topbar_frame = tkb.Frame(self, background=self.topbar_bg_color)
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame,
            text="User Form",
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.title_lb.pack(side="left", padx=10)
