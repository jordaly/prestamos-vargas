import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Any


class Event:
    def __init__(self, name: str, trigger: str, data: Any):
        self.name = name
        self.trigger = trigger
        self.data = data

    def __str__(self):
        return f"event: ({self.name}) from ({self.trigger})"


class TestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("layout example")
        self.geometry("600x400")

        # self.style = ttk.Style()
        # self.style.theme_use("clam")

        self.main_frame = ttk.Frame(self).pack(expand=True, fill="both")

        self.result_lb = ttk.Label(
            self.main_frame, text="Welcome to the main window"
        ).pack(expand=True)

        self.second_window_btn = ttk.Button(
            self.main_frame, text="Second Window", command=lambda: self.second_window()
        ).pack(expand=True)

    def second_window(self):
        self.top = SecondWindow(self.listen_event)

    def listen_event(self, event: Event):
        print(event)
        print(event.data)


class SecondWindow(tk.Toplevel):
    def __init__(self, listen_event):
        super().__init__()

        self.title("Second Window")
        self.geometry("300x200")

        self.listen_event = listen_event
        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True)

        self.label = ttk.Label(self.frame, text="Welcome to the second window")
        self.label.pack()
        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.pack()
        self.submit_btn = ttk.Button(self.frame, text="Submit", command=self.send_event)
        self.submit_btn.pack()

        self.back_btn = ttk.Button(self.frame, text="Back", command=self.back)
        self.back_btn.pack()

    def send_event(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        data = {"name": name}
        event = Event("entered_name", "second_window", data)

        self.listen_event(event)
        self.destroy()

    def back(self):
        self.destroy()


if __name__ == "__main__":
    TestApp().mainloop()
