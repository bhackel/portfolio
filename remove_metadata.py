import os
from PIL import Image

def remove_metadata(image_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Convert the image to remove metadata (EXIF)
        data = list(img.getdata())
        img_no_metadata = Image.new(img.mode, img.size)
        img_no_metadata.putdata(data)

        # Save the image, overwriting the original file
        img_no_metadata.save(image_path)
        print(f"Metadata removed and image saved: {image_path}")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def process_images(folder_path):
    # Walk through the folder and all subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is an image by file extension
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
                image_path = os.path.join(root, file)
                remove_metadata(image_path)

if __name__ == "__main__":
    # Get the current directory
    current_directory = os.getcwd()

    # Process all images in the current directory and subfolders
    process_images(current_directory)
