'''
This program will decode the message which is stored in the image
The image wth the message is encoded_image.py
'''

from PIL import Image
import numpy as np
import base64
import os
import sys
import hashlib


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
        
    # extraction of the binary message upto the delimitter
    binary_message = binary_message[:end_index]
    
    # convert the binary message to character
    message_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join([chr(int(byte, 2)) for byte in message_bytes])
    
    # separate and decode the original message and hash
    separate_index = message.rfind("=")+1
    message_encode, message_hash = message[:separate_index], message[separate_index:]
    
    # Decoding the base64 encoded image
    message_encode = base64.b64decode(message_encode).decode('utf-8')
    
    # verification of intergrity of the message using the hash
    if hashlib.sha256(message_encode.encode()).hexdigest() != message_hash:
        print("The message has been tampered with")
        sys.exit(1)
    else:
        print('Message has been decoded successful')