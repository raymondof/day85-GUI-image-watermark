import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image


root = Tk()
root.title("Watermark your photo")
root.geometry("1000x900")
root.grid_rowconfigure(1, weight=1) # Allow row 0 to expand
root.grid_columnconfigure(0, weight=1) # Allow column 0 to expand

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, padx=10, pady=10, sticky=(N, W, E, S))

filepath_var = StringVar(master=None)
filepath_var.set("No file selected")

# Create a label for displaying the image
image_label = ttk.Label(root)
image_label.grid(column=0, row=1, columnspan=4, pady=10)

def open_image(image_path):
    # Open an image using Pillow (JPG reads as <class 'PIL.JpegImagePlugin.JpegImageFile'>)
    image = Image.open(image_path)

    # Calculate new dimensions while preserving the original aspect ratio
    width, height = image.size
    desired_short_side = 600

    if height > width:
        # Calculate the new height based on the desired width
        new_height = int(desired_short_side * (height / width))

        # Resize the image with the fixed width and calculated height
        image = image.resize((desired_short_side, new_height))
    elif height < width:
        new_width = int(desired_short_side * (width / height))
        image = image.resize((new_width, desired_short_side))


    # Convert the image to a PhotoImage (<class 'PIL.ImageTk.PhotoImage'>)
    image_tk = ImageTk.PhotoImage(image)
    print(f"image_tk: {type(image_tk)}")

    # Create a label to display the image
    image_label.configure(image=image_tk)
    image_label.image = image_tk
def upload_action(event=None):
    global filepath_var
    filepath = filedialog.askopenfilename()
    print("Selected:", filepath)
    print("Which type is:", type(filepath))
    filepath_var.set(filepath)
    open_image(filepath)

# Set button
add_file_button = tkinter.Button(root, text="Open file", command=upload_action)
add_file_button.grid(column=3, row=0)

# Set labels
ttk.Label(mainframe, text="Filename").grid(column=1, row=0, padx=(0,10))
ttk.Label(mainframe, textvariable=filepath_var).grid(column=2, row=0)



root.mainloop()