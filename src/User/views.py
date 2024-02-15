import ttkbootstrap as tkb
from ttkbootstrap import constants

style = tkb.Style.get_instance()
style.configure("topbar_content_bg_color.TFrame", background="#CCC")


class UserView(tkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.panel = UserPanel(self)
        self.form = UserForm(self)
        self.panel.pack(expand=True, fill=constants.BOTH)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.forget()

    def go_to_user_form(self):
        self.clear_frame()
        self.form.pack(expand=True, fill=constants.BOTH)

    def go_to_user_panel(self):
        self.clear_frame()
        self.panel.pack(expand=True, fill=constants.BOTH)


class UserPanel(tkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure_grid()

        self.load_topbar()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=0, minsize=50)
        self.rowconfigure(index=1, weight=1)

    def load_topbar(self):
        self.topbar_frame = tkb.Frame(self, style="topbar_content_bg_color.TFrame")
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame,
            text="Users Panel",
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.title_lb.pack(side="left", padx=10)


class UserForm(tkb.Frame):
    def __init__(self, parent, new: bool = False):
        super().__init__(parent)
        self.parent = parent
        self.configure_grid()

        self.load_topbar()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=0, minsize=100)
        self.rowconfigure(index=0, weight=1)

    def load_topbar(self):
        self.topbar_frame = tkb.Frame(self, style="topbar_content_bg_color.TFrame")
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame,
            text="User Form",
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.title_lb.pack(side="left", padx=10)
