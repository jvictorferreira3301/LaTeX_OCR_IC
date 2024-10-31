import cv2
import os
from pathlib import Path
from PIL import Image
import numpy as np

def pad(img: Image, divable=32): 
    """Pad an Image to the next full divisible value of `divable`. Also normalizes the image and inverts if needed. 
    Args: 
        img (PIL.Image): input image 
        divable (int, optional): . Defaults to 32. 
    Returns: 
        PIL.Image 
    """ 
    data = np.array(img.convert('LA')) 
    data = (data - data.min()) / (data.max() - data.min()) * 255 
    if data[..., 0].mean() > 128: 
        gray = 255 * (data[..., 0] < 128).astype(np.uint8)  # To invert the text to white 
    else: 
        gray = 255 * (data[..., 0] > 128).astype(np.uint8) 
        data[..., 0] = 255 - data[..., 0] 

    coords = cv2.findNonZero(gray)  # Find all non-zero points (text) 
    a, b, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box 
    rect = data[b:b+h, a:a+w] 
    if rect[..., -1].var() == 0: 
        im = Image.fromarray((rect[..., 0]).astype(np.uint8)).convert('L') 
    else: 
        im = Image.fromarray((255 - rect[..., -1]).astype(np.uint8)).convert('L') 
    dims = [] 
    for x in [w, h]: 
        div, mod = divmod(x, divable) 
        dims.append(divable * (div + (1 if mod > 0 else 0))) 
    padded = Image.new('L', dims, 255) 
    padded.paste(im, im.getbbox()) 
    return padded 

def convert_images(input_dir, output_dir):
    """Convert all images in the input directory to grayscale and save in the output directory."""
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process each image file in the input directory
    for img_file in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_file)
        
        # Check if the file is a PNG image
        if img_path.endswith('.png'):
            # Read the image with PIL
            img = Image.open(img_path)
            pad_img = pad(img)

            # Convert the padded image back to a NumPy array for saving with OpenCV
            pad_img_np = np.array(pad_img)
            
            # Create output file path
            output_path = os.path.join(output_dir, img_file)
            
            # Save the grayscale image using OpenCV
            cv2.imwrite(output_path, pad_img_np)
            print(f"Converted and saved: {output_path}")

# Usage
input_dir = 'outputs/images'  # Replace with the path to your input images
output_dir = 'outputs/images_pad'  # Replace with the path for output images

convert_images(input_dir, output_dir)
