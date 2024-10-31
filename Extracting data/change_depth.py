import cv2
import os
from pathlib import Path

def convert_images_to_grayscale(input_dir, output_dir):
    """Convert all images in the input directory to grayscale and save in the output directory."""
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process each image file in the input directory
    for img_file in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_file)
        
        # Check if the file is an image
        if img_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Read the image
            bgr_img = cv2.imread(img_path)
            if bgr_img is None:
                print(f"Skipping {img_file}: not a valid image.")
                continue
            
            # Convert the image to grayscale
            gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

            # Create output file path
            output_path = os.path.join(output_dir, img_file)
            
            # Save the grayscale image
            cv2.imwrite(output_path, gray_img)
            print(f"Converted and saved: {output_path}")

# Usage
input_dir = 'outputs/images'  # Replace with the path to your input images
output_dir = 'outputs/images_8'  # Replace with the path for output images

convert_images_to_grayscale(input_dir, output_dir)
