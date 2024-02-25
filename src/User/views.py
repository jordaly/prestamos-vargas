import ttkbootstrap as tkb
from ttkbootstrap import constants
from database.models import User

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
        self.load_content()

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=0, minsize=50)
        self.rowconfigure(index=1, weight=1)

    def load_topbar(self):
        style = tkb.Style.get_instance()
        style.configure(
            "topbarContentLabel.TLabel", background="#CCC", foreground="black"
        )
        self.topbar_frame = tkb.Frame(self, style="topbar_content_bg_color.TFrame")
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame, text="Users Panel", style="topbarContentLabel.TLabel"
        )
        self.title_lb.pack(side=constants.LEFT, padx=10)

        self.new_user_btn = tkb.Button(
            self.topbar_frame,
            text="New",
            command=lambda: self.new_user(),
            bootstyle=constants.DARK,
        )
        self.new_user_btn.pack(side=constants.RIGHT, padx=10)

        self.search_bth = tkb.Button(
            self.topbar_frame, text="Search", bootstyle=constants.DARK
        )
        self.search_bth.pack(side=constants.RIGHT, padx=10)

        self.search_bar = tkb.Entry(self.topbar_frame)
        self.search_bar.pack(side=constants.RIGHT, padx=10)

    def load_content(self):
        self.content = tkb.Frame(self)
        self.content.grid(column=0, row=1, sticky="nsew")
        self.table = tkb.Treeview(
            self.content,
            columns=("id", "username", "email", "first", "last"),
            show="headings",
            bootstyle=constants.DARK,
        )

        self.table.heading("id", text="ID")

        self.table.heading("username", text="Username")
        self.table.heading("email", text="Email")
        self.table.heading("first", text="First Name")
        self.table.heading("last", text="Last Name")

        self.table.column("id", width=50, anchor=constants.CENTER)
        self.table.column("username", width=100, anchor=constants.CENTER)
        self.table.column("email", width=100, anchor=constants.CENTER)
        self.table.column("first", width=100, anchor=constants.CENTER)
        self.table.column("last", width=100, anchor=constants.CENTER)

        users = User.all()

        print(users)

        for user in users:
            self.table.insert(
                parent="",
                index=constants.END,
                iid=user.id,
                values=(
                    user.id,
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                ),
            )

        self.table.pack(expand=True, fill=constants.BOTH)


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
