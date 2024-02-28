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
        self.panel.clean()
        self.panel.pack(expand=True, fill=constants.BOTH)


class UserPanel(tkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure_grid()

        self.load_topbar()
        self.load_content()

    def new_user(self):
        self.parent.clear_frame()
        self.parent.form.pack(expand=True, fill=constants.BOTH)

    def configure_grid(self):
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=0, minsize=50)
        self.rowconfigure(index=1, weight=1)

    def load_topbar(self):
        style = tkb.Style.get_instance()
        style.configure(
            "topbarContentLabel.TLabel", background="#CCC", foreground="black"
        )

        self.search_bar_var = tkb.StringVar()

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
            self.topbar_frame,
            text="Search",
            bootstyle=constants.DARK,
            command=lambda: self.load_tree_data(username=self.search_bar_var.get()),
        )

        self.search_bth.pack(side=constants.RIGHT, padx=10)

        self.search_bar = tkb.Entry(self.topbar_frame, textvariable=self.search_bar_var)

        self.search_bar.bind(
            sequence="<Return>",
            func=lambda _: self.load_tree_data(username=self.search_bar_var.get()),
        )

        self.search_bar.bind(
            sequence="<KeyRelease>",
            func=lambda _: self.load_tree_data(username=self.search_bar_var.get()),
        )

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

        self.table.pack(expand=True, fill=constants.BOTH)

        self.load_tree_data()

    def load_tree_data(self, username: str = None):
        for item in self.table.get_children():
            self.table.delete(item)

        users = User.filter(username=username) if username else User.all()

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

    def clean(self):
        self.search_bar_var.set("")
        self.load_tree_data()


class UserForm(tkb.Frame):
    def __init__(self, parent, new: bool = False):
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
        self.topbar_frame = tkb.Frame(self, style="topbar_content_bg_color.TFrame")
        self.topbar_frame.grid(column=0, row=0, sticky="nsew")

        self.title_lb = tkb.Label(
            self.topbar_frame,
            text="User Form",
            bootstyle=(constants.DARK, constants.INVERSE),
        )
        self.title_lb.pack(side="left", padx=10)

        self.cancel_btn = tkb.Button(
            self.topbar_frame,
            text="Cancel",
            command=lambda: self.parent.go_to_user_panel(),
            bootstyle=constants.DARK,
        )
        self.cancel_btn.pack(side="right", padx=10)

        self.save_btn = tkb.Button(
            self.topbar_frame,
            text="Save",
            command=lambda: self.save_user(),
            bootstyle=constants.DARK,
        )

        self.save_btn.pack(side="right", padx=10)

    def load_content(self):
        style.configure("form.TFrame")

        self.content = tkb.Frame(self)
        self.content.grid(column=0, row=1, sticky="nsew")

        self.username_frame = tkb.Frame(self.content, style="form.TFrame")
        self.username_lb = tkb.Label(self.username_frame, text="Username")
        self.username_var = tkb.StringVar()
        self.username_entry = tkb.Entry(
            self.username_frame, textvariable=self.username_var
        )
        self.username_lb.pack()
        self.username_entry.pack()

        self.password_frame = tkb.Frame(self.content, style="form.TFrame")
        self.password_lb = tkb.Label(self.password_frame, text="Password")
        self.password_var = tkb.StringVar()
        self.password_entry = tkb.Entry(
            self.password_frame, textvariable=self.password_var
        )
        self.password_lb.pack()
        self.password_entry.pack()

        self.email_frame = tkb.Frame(self.content, style="form.TFrame")
        self.email_lb = tkb.Label(self.email_frame, text="Email")
        self.email_var = tkb.StringVar()
        self.email_entry = tkb.Entry(self.email_frame, textvariable=self.email_var)
        self.email_lb.pack()
        self.email_entry.pack()

        self.first_name_frame = tkb.Frame(self.content, style="form.TFrame")
        self.first_name_lb = tkb.Label(self.first_name_frame, text="First Name")
        self.first_name_var = tkb.StringVar()
        self.first_name_entry = tkb.Entry(
            self.first_name_frame, textvariable=self.first_name_var
        )
        self.first_name_lb.pack()
        self.first_name_entry.pack()

        self.last_name_frame = tkb.Frame(self.content, style="form.TFrame")
        self.last_name_lb = tkb.Label(self.last_name_frame, text="Last Name")
        self.last_name_var = tkb.StringVar()
        self.last_name_entry = tkb.Entry(
            self.last_name_frame, textvariable=self.last_name_var
        )
        self.last_name_lb.pack()
        self.last_name_entry.pack()

        self.username_frame.pack(pady=10)
        self.password_frame.pack(pady=10)
        self.email_frame.pack(pady=10)
        self.first_name_frame.pack(pady=10)
        self.last_name_frame.pack(pady=10)

    def save_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        email = self.email_var.get()
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()

        user = User(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.save()
