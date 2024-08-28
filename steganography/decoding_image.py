'''
This program will decode the message which is stored in the image
The image wth the message is encoded_image.py
'''

from PIL import Image
import numpy as np
import base64
import os
import sys


# printing out the current working directory and listing the files 
print("Present Working Directory: ", os.getcwd())
print("Files in steganography folder:", os.listdir('C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography'))

# A function to decode the image
def decode_image(image_path, message, output_image_path):
    # Open the image using PIL
    try:
        encoded_image_to_open = Image.open(image_path)
        encoded_image_to_open =encoded_image_to_open.convert("RGB")
    except FileNotFoundError as e:
        print("The file {image_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print("Sorry, an error occurred: ", e)
    
    # Convert the image to numpy array
    image_array = np.array(encoded_image_to_open)
    
    # Flattening the image to enable you work well with
    flattened_data = image_array.flatten()
    
    #  extraction of the least significant bits fom te pixels values
    binary_message = ''.join([str(pixel & 1) for pixel in flattened_data ])
    
    # highlighting the delimitter which shows the end of the message encode
    delimitter = '1111111111111110'
    end_index = binary_message.find(delimitter)
    
    if end_index == 1:
        print("No message found in the image")
        sys.exit(1)