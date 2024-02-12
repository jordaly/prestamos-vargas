from app import App
from database.db import create_database

if __name__ == "__main__":
    create_database()

    app = App(title="Prestamos Vargas", size=(500, 300), icon_path="img/logo.png")

    app.mainloop()
