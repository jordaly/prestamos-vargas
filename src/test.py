import settings
import ttkbootstrap as tkb


window = tkb.Window(title="test")
window.geometry("800x600")

# Load the Image
image_path = settings.CURRENT_PATH / "assets" / "img" / "logo.png"
photo = tkb.ImageTk.PhotoImage(tkb.Image.open(image_path))

# Create the Label
label = tkb.Label(window, image=photo)
label.pack()

window.mainloop()
