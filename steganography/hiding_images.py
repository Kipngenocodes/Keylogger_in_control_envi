from PIL import Image
import numpy as np
import base64
import hashlib
import os
import sys

# Print current working directory and list files
print("Current working directory:", os.getcwd())
print("Files in steganography folder:", os.listdir('C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography'))

# A function to encode the message 
def encode_message(image_path, message, out_image_path):
    # Open the image
    try:
        image_opening = Image.open(image_path)
        image_opening = image_opening.convert("RGB")
    except FileNotFoundError as e:
        print(f'Error: The file {image_path} was not found.')
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        sys.exit(1)
        
    # Converting the image to a numpy array
    image_array = np.array(image_opening)
    
    # Encode the message to base64 to ensure safe character handling
    message_encoded = base64.b64encode(message.encode('utf-8')).decode('utf-8')

    # Create a hash of the message for integrity verification
    message_hash = hashlib.sha256(message_encoded.encode()).hexdigest()

    # Converting the message and its hash into binary
    message_binary = ''.join(format(ord(i), '08b') for i in message_encoded + message_hash) + '1111111111111110'  # Delimiter to mark the end
    
    # Checking if the image can store the message accurately
    if len(message_binary) > image_array.size * 3:
        raise ValueError("Message is too long to hide in this image")
    
    # Flattening the array to iterate over the image pixels
    data_flatten = image_array.flatten()
        
    # Encode the message in the least significant bit of the pixels
    for i in range(len(message_binary)):
        # Modify the LSB of the pixel value correctly
        data_flatten[i] = (data_flatten[i] & 0b11111110) | int(message_binary[i])
        
    # Reshaping array to its original form
    image_array = data_flatten.reshape(image_array.shape)
    
    # Saving the encoded image
    try:
        encoded_image = Image.fromarray(image_array.astype(np.uint8))  # Ensure correct data type
        encoded_image.save(out_image_path)
        print(f'Message encoded and saved as {out_image_path}')
    except Exception as e:
        print(f"An error occurred while saving the encoded image: {e}")
        sys.exit(1)
    
# Using an image
image_path = 'C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography\\picture.png'  # Ensure this path is correct
message = "You will be hacked one day unless you watch what is necessary. I am"
out_image_path = 'C:\\Users\\Admin Pc\\Desktop\\project_60\\steganography\\encoded_image.png'  # Output path

# Encode the message
encode_message(image_path, message, out_image_path)
