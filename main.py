from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk, ImageDraw, ImageFont


window = Tk()
window.title("Image Watermarker")
window.minsize(width=800, height=500)

uploaded_image = None
displayed_image = None
watermarked_image = None
def upload_file():
    global uploaded_image
    global displayed_image
    filetypes = (
        ('Image files', ('*.jpg', '*.jpeg', '*.png')),
        )
    file_path = filedialog.askopenfilename(title="Open File",filetypes=filetypes)

    uploaded_image = Image.open(file_path)
    display_image(uploaded_image)


def display_image(image):
    # Open the image using Pillow

    image.thumbnail((600,600))

    displayed_image = ImageTk.PhotoImage(image)  # Convert the image to a PhotoImage

    # Update the label to display the image
    image_label.config(image=displayed_image)
    image_label.image = displayed_image  # Keep a reference to avoid garbage collection


def add_wmark():
    global uploaded_image
    global watermarked_image

    if uploaded_image.mode != 'RGBA':
        uploaded_image = uploaded_image.convert('RGBA')

    wmark_text = str(wmark_entry.get())

    x,y = map(float, place_entry.get().split(","))
    print(x,y)

    # Set the text color with the desired opacity (RGBA)
    txt_layer = Image.new("RGBA",uploaded_image.size, (255,255,255,0))

    draw = ImageDraw.Draw(txt_layer)
    font = ImageFont.truetype('arial.ttf', size=50)

    opacity = int(opacity_entry.get())

    text_color = (255,255,255,opacity)

    draw.text((x,y), wmark_text, font=font, fill=text_color)

    watermarked_image = Image.alpha_composite(uploaded_image, txt_layer)

    display_image(watermarked_image)


def save_image():
    global watermarked_image
    if watermarked_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:  # Check if a file was selected
            watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")
    else:
        messagebox.showwarning("Warning", "No image to save!")




my_label = Label(text="Watermark your Image", font=("Arial", 20, "bold"))
my_label.grid(row = 0, column = 0, padx = 5, pady = 5)

image_entry = Entry()
image_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
image_entry.config(width=50)

upload = Button(text="Upload", command=upload_file)
upload.grid(row = 1, column = 1, padx = 5, pady = 5)

image_label = Label()
image_label.grid(row = 2, column = 0, padx = 5, pady = 5 )

wmark = Label(text="Enter Watermark text: ")
wmark.grid(row = 3, column = 0, padx = 5, pady = 5 )

wmark_entry = Entry(width=20)
wmark_entry.grid(row = 3, column = 1, padx = 5, pady = 5 )

place = Label(text="Enter the coordinates to place: ")
place.grid(row = 4, column = 0, padx = 10, pady = 10 )

place_entry = Entry(width=20)
place_entry.grid(row = 4, column = 1, padx = 10, pady = 10 )

opacity = Label(text="Enter Opacity 0-255")
opacity.grid(row = 5, column = 0, padx = 10, pady = 10)

opacity_entry = Entry(width=20)
opacity_entry.grid(row = 5, column = 1, padx = 10, pady = 10)

submit = Button(text="Submit", command=add_wmark)
submit.grid(row = 6, column = 0, padx = 10, pady = 10)

save = Button(text="Save Image", command=save_image)
save.grid(row = 7, column = 0, padx = 10, pady = 10)


window.mainloop()