import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import ImageFont
from PIL import ImageDraw
import os

# Create the main Tkinter window
root = Tk()
root.title("Watermark your photo")
root.geometry("1000x900")
root.grid_rowconfigure(3, weight=3)  # Allow row 3 to expand (the image)
# root.grid_columnconfigure(0, weight=3)  # Allow column 0 to expand

# Create a frame within the main window
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, padx=10, pady=10)

# Variables to store file paths and display text in labels
img_filepath_var = StringVar(master=None)
img_filepath_var.set("No file selected")
img_filepath = ""

logo_filepath_var = StringVar(master=None)
logo_filepath_var.set("beer_logo.png")
logo_filepath = "/home/raimo/PycharmProjects/day85-GUI-image-watermark/logos/beer_logo.png"

# Create a label for displaying the image
image_label = ttk.Label(root)
image_label.grid(column=0, row=3, columnspan=4, pady=10)


def return_file_name(filepath):
    """Function to split a file path and return the file name without extension"""
    # Use os.path to split the file path
    file_dir, file_name = os.path.split(filepath)

    # Split the file name from its extension
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    return file_name_without_extension, file_extension


def add_logo_on_image():
    """Function to add logo on image"""
    global img_filepath
    # Open image that is currently visible (in case it is open) and make a copy of it
    image = Image.open(img_filepath)
    wm_logo_image = image.copy()
    width, height = wm_logo_image.size
    x = width - 200

    # Open logo image
    logo_image = Image.open(logo_filepath)
    logo_image = logo_image.resize((200, 200))

    # Destination, image to paste, coordinates, transparency mask
    wm_logo_image.paste(logo_image, (x, 0), logo_image)

    img_name, img_extension = return_file_name(img_filepath)
    logo_name, logo_extension = return_file_name(logo_filepath)

    wm_img_logo_path = "images_with_logo/" + img_name + "_" + logo_name + img_extension
    wm_logo_image.save(wm_img_logo_path)
    open_image(wm_img_logo_path)


def add_text_on_image():
    """Function to add text to an image"""
    global img_filepath
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf", 40)
    image = Image.open(img_filepath)

    watermark_image = image.copy()
    draw = ImageDraw.Draw(watermark_image)
    width, height = watermark_image.size

    # Get input text from entry field
    wm_text = text_input.get()
    draw.text((width/2, 100), wm_text, fill=(255, 255, 255), font=font, anchor="ms")

    img_name, img_extension = return_file_name(img_filepath)

    wm_image_path = "images_with_text/" + img_name + wm_text + img_extension
    img_filepath = wm_image_path
    watermark_image.save(wm_image_path)
    open_image(wm_image_path)


def open_image(image_path):
    """Function to open and display an image"""
    # Open an image using Pillow (JPG reads as <class 'PIL.JpegImagePlugin.JpegImageFile'>)
    image = Image.open(image_path)

    # Calculate new dimensions while preserving the original aspect ratio
    width, height = image.size
    desired_short_side = 600

    if height > width:
        # Calculate the new height based on the desired short side
        new_height = int(desired_short_side * (height / width))

        # Resize the image with the fixed width and calculated height
        image = image.resize((desired_short_side, new_height))
    elif height < width:
        new_width = int(desired_short_side * (width / height))
        image = image.resize((new_width, desired_short_side))

    # Convert the image to a PhotoImage (<class 'PIL.ImageTk.PhotoImage'>)
    image_tk = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label.configure(image=image_tk)
    image_label.image = image_tk


def upload_image():
    """Function to upload an image"""
    global img_filepath_var, img_filepath
    img_filepath = filedialog.askopenfilename()
    print("Selected:", img_filepath)
    print("Which type is:", type(img_filepath))
    img_filepath_var.set(img_filepath)
    open_image(img_filepath)


def upload_logo():
    """Function to upload a logo image"""
    global logo_filepath_var, logo_filepath
    logo_filepath = filedialog.askopenfilename()
    print("Selected:", logo_filepath)
    print("Which type is:", type(logo_filepath))
    logo_name, logo_extension = return_file_name(logo_filepath)
    logo_filepath_var.set(logo_name + logo_extension)


# Set buttons
add_file_button = tkinter.Button(mainframe, width=8, text="Open file", command=upload_image)
add_file_button.grid(column=2, row=0, sticky=W, padx=2)

add_text_button = tkinter.Button(mainframe, width=8, text="Add text", command=add_text_on_image)
add_text_button.grid(column=2, row=1, sticky=W, padx=2)

open_logo_button = tkinter.Button(mainframe, width=8, text="Open logo", command=upload_logo)
open_logo_button.grid(column=2, row=2, sticky=W, padx=2)

add_logo_button = tkinter.Button(mainframe, width=8, text="Add logo", command=add_logo_on_image)
add_logo_button.grid(column=3, row=2, padx=2)

# Set labels
ttk.Label(mainframe, text="Filename: ").grid(column=0, row=0, sticky=E)
ttk.Label(mainframe, textvariable=img_filepath_var).grid(column=1, row=0, sticky=W)

ttk.Label(mainframe, text="Watermark text:").grid(column=0, row=1)

ttk.Label(mainframe, text="Logo file: ").grid(column=0, row=2, sticky=E)
ttk.Label(mainframe, textvariable=logo_filepath_var).grid(column=1, row=2, sticky=W)

# Text entry fields
text_input = Entry(mainframe, width=70)
text_input.grid(column=1, row=1)

root.mainloop()
