from app import App
from database.db import create_database
import asyncio


if __name__ == "__main__":
    create_database()

    app = App(title="Prestamos Vargas", size=(500, 300), icon_path="img/logo.png")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.mainloop_async())
