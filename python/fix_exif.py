# This is a Python script that processes images and extracts EXIF data from them, and writes missing image_width and image_length exif data. 
# Here's a breakdown of what the script does:

# It imports necessary libraries:
# os for interacting with the file system
# argparse for parsing command-line arguments
# PIL (Python Imaging Library) for image processing
# exif library for working with EXIF data
# The script defines several functions:
# get_exif_data: extracts EXIF data from an image file
# 
# get_image_dimensions: gets the width and length of an image from its EXIF data
# 
# update_exif_with_dimensions: updates the EXIF data with the new width and height of an image
# 
# The script defines a main function process_input that:
# 
# If the input is a directory, processes all images in it
# 
# If the input is a single file, processes its EXIF data and updates it if necessary
# 
# The script uses command-line arguments to specify the path to the image directory or file.
# 
# To use this script, simply save it as a Python file (e.g., exif_process.py) and run it from the command line with the path to an image directory or file as an argument:

# Bash
# Insert code

# $ python exif_process.py /path/to/image/directory
# or

# Bash
# Insert code

# $ python exif_process.py /path/to/image/file.jpg
# Note that this script assumes that the images are in a format that supports EXIF data (e.g., JPEG, PNG). If you need to support other formats, you may need to modify the script accordingly.

import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from exif import Image as ExifImage
from PIL import Image as PillowImage
from PIL import ExifTags


# Function to extract EXIF data from an image
def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if exif_data is not None:
            # Translate EXIF tags to readable format
            exif = {TAGS.get(tag): value for tag, value in exif_data.items()}
            return exif
        else:
            return None
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None

# Function to get image width and length from EXIF data
def get_image_dimensions(exif):
    if exif:
        width = exif.get('ImageWidth')
        length = exif.get('ImageLength')
        return width, length
    return None, None

# Function to update EXIF data with width and height using the exif library
def update_exif_with_dimensions(image_path, width, height):
    try:
        # Load existing EXIF data
        with open(image_path, 'rb') as img_file:
            img = ExifImage(img_file)

        # Set width and height in the Exif data
        # img.set('image_width', width)
        
        # img.image_width = width

        # Save the updated EXIF data back to the image
        # with open(image_path, 'wb') as img_file:
            # img.save(img_file)

        print(img.has_exif)
        print(img.list_all())

        # image_path = "without-metadata/{}".format(img)
        pillow_image = PillowImage.open(image_path)
        img_exif = pillow_image.getexif()
        img_exif[ExifTags.Base.ImageWidth] = width
        img_exif[ExifTags.Base.ImageLength] = height

        # with open('modified_image.jpg', 'wb') as new_image_file:
        pillow_image.save(image_path, exif=img_exif)


        print(f"Updated EXIF data for {image_path} with width: {width}, height: {height}.")
    except Exception as e:
        print(f"Failed to update EXIF data for {image_path}: {e}")

# Main function to process the input (directory or file)
def process_input(path):
    if os.path.isdir(path):
        # Process images in the directory
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            # Check if it's a valid image file
            if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                exif_data = get_exif_data(file_path)

                if exif_data:
                    width, length = get_image_dimensions(exif_data)

                    if width and length:
                        print(f"Image: {filename}")
                        print(f"Width: {width}, Length: {length}\n")
                    else:
                        print(f"Image: {filename} has no EXIF width/length data, reading from image...\n")
                        img = Image.open(file_path)
                        width, height = img.size
                        update_exif_with_dimensions(file_path, width, height)
                else:
                    print(f"Image: {filename} has no EXIF data.\n")
    elif os.path.isfile(path) and path.lower().endswith(('.jpg', '.jpeg', '.png')):
        # Process the single image file
        exif_data = get_exif_data(path)
        
        if exif_data:
            width, length = get_image_dimensions(exif_data)
            if width and length:
                print(f"Image: {os.path.basename(path)}")
                print(f"Width: {width}, Length: {length}\n")
            else:
                print(f"Image: {os.path.basename(path)} has no EXIF width/length data, reading from image...\n")
                img = Image.open(path)
                width, height = img.size
                update_exif_with_dimensions(path, width, height)
        else:
            print(f"Image: {os.path.basename(path)} has no EXIF data.\n")
    else:
        print(f"The path {path} is not a valid directory or image file.")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process images to show EXIF width and length.")
    parser.add_argument('path', type=str, help='The path to the image directory or image file.')

    # Parse the arguments
    args = parser.parse_args()

    # Process the input
    process_input(args.path)
