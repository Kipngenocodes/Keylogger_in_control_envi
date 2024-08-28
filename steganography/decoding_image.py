'''
This program will decode the message which is stored in the image
The image wth the message is encoded_image.py
'''


from PIL import Image
import numpy as np
import base64
import hashlib
import os
import sys

# Print the current working directory and list files in the folder
print("Current Working Directory:", os.getcwd())
print("Files in steganography folder:", os.listdir('C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography'))

# Function to decode the message from the image
def decode_image(image_path):
    # Open the image using PIL
    try:
        encoded_image_to_open = Image.open(image_path)
        encoded_image_to_open = encoded_image_to_open.convert("RGB")
    except FileNotFoundError:
        print(f"The file {image_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Sorry, an error occurred: {e}")
        sys.exit(1)
    
    # Convert the image to a numpy array
    image_array = np.array(encoded_image_to_open)
    
    # Flatten the array to work with pixel values
    flattened_data = image_array.flatten()
    
    # Extract the least significant bits from the pixel values
    binary_message = ''.join([str(pixel & 1) for pixel in flattened_data])
    
    # Find the delimiter that marks the end of the message
    delimiter = '1111111111111110'
    end_index = binary_message.find(delimiter)
    
    if end_index == -1:
        print("No message found in the image.")
        sys.exit(1)
    
    # Extract the binary message up to the delimiter
    binary_message = binary_message[:end_index]
    
    # Convert the binary message to characters
    message_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join([chr(int(byte, 2)) for byte in message_bytes])
    
    try:
        # Separate and decode the original message and hash
        separator_index = message.rfind("=") + 1
        message_encoded, message_hash = message[:separator_index], message[separator_index:]
        
        # Decode the base64 encoded message
        message_decoded = base64.b64decode(message_encoded).decode('utf-8')
        
        # Verify the integrity of the message using the hash
        if hashlib.sha256(message_encoded.encode()).hexdigest() != message_hash:
            print("Warning: The message has been tampered with.")
            sys.exit(1)
        else:
            print('Message decoded successfully.')
        print(f"Decoded message: {message_decoded}")
    except Exception as e:
        print(f"An error occurred while decoding the message: {e}")
        sys.exit(1)

# Path to the encoded image
encoded_image_path = 'C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography\\encoded_image.png'

# Decode the message
decode_image(encoded_image_path)
