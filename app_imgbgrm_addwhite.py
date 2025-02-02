#Help https://pyseek.com/2024/10/how-to-remove-image-background-using-python/
#https://www.geeksforgeeks.org/python-pil-image-resize-method/
#https://pixelphant.com/blog/perfect-background-for-product-photography
#https://pathedits.com/blogs/tips/how-should-i-choose-the-color-for-my-product-background

import io
from io import BytesIO
import streamlit as st
from PIL import Image,  ImageOps
from rembg import remove
from pathlib import Path

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](<https://github.com/tyler-simons/BackgroundRemoval>) on GitHub. Special thanks to the [rembg library](<https://github.com/danielgatis/rembg>) :grin:"
)
st.sidebar.write("## Upload and download :gear:")

# Create the columns
col1, col2 = st.columns(2)

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Package the transform into a function
def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)
        
    # Remove the background
    output_data = remove(image)
    
    #Convert to image
    fix_image = convert_image(output_data)

    # Load fixed image
    output_image = Image.open(BytesIO(fix_image))

    #resize image
    #newsize = (1000, 1000)
    #output_image = output_image.resize (newsize)
    width = 1500
    height = int(output_image.height * (width / output_image.width))
    output_image_resize = output_image.resize((width, height), Image.LANCZOS)
    
    # Create a solid background (white)
    
    new_background = Image.new('RGB', output_image_resize.size, (255, 255, 255))

    # Paste the image without the background on top of the white background
    new_background.paste(output_image_resize, mask=output_image_resize.split()[3])
    
    # Save the final image
    output_path = str( (file.stem +".out.png"))
    download_img = Image.open(BytesIO(convert_image(new_background))) 
    #new_background.save(output_path)
    #The quality parameter ranges from 1 (worst) to 95 (best).
    #download_img.save(output_path, quality=)
    # Save the image with optimization
    download_img.save(output_path, quality=95)


    col2.write(output_path)
    col2.image(new_background)
    st.sidebar.markdown("\\n")
    #st.sidebar.download_button(
    #    "Download fixed image", download_img, "fixed.png", "image/png"
    #)

# Create the file uploader
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Path to input directory
INPUT_DIR = Path.cwd() / "productos_originales"
OUTPUTDIR = Path.cwd() / "productos_corregidos"

# Fix the image!
if my_upload is not None:
    fix_image(upload=my_upload)
else:
    for file in list(INPUT_DIR.rglob("*.JPG*")):
        print (file)
        fix_image(file)
    
    








