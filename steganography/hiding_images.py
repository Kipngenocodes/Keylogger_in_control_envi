#  this program will hide a message in an image
#  the message will be hidden in the least significant bits of the pixels
# 

from PIL import Image
import numpy as np
import os
import sys
import argparse
import base64
import hashlib

#  a function to encode the message 
def encode_message(image_path, message, out_image_path):
    #  open the image
    try:
        image_opening = Image.open(image_path)
        image_opening = image_opening.convert("RGB")
    except FileNotFoundError as e:
        print(f'Error: The file {image_path} was not found.')
        sys.exit(1)
        
    # Converting an image to numpy array
    image_array = np.array(image_opening)
    
    # Encode the message to base64 to ensure safe character handling
    message_encoded = base64.b64encode(message.encode('utf-8')).decode('utf-8')

    # Create a hash of the message for integrity verification
    message_hash = hashlib.sha256(message_encoded.encode()).hexdigest()

    # converting the message into binary
    message_binary = (
                        ''.join(format(ord(i), '08b') for i in message + message_hash) + '1111111111111110'
                    ) 
    
    # checking if the image to assess it it can store the message accurately
    if len(message_binary) > image_array.size*3:
        raise ValueError("Message is too long to hide in this image")
    
    #  flattemig the array to iterate over the image pixel
    data_flatten = image_array.flatten()
        
    # Encode the message in pixels
    for i in range(len(message_binary)):
        #  get the binary of the pixel
        data_flatten [i]= format(data_flatten[i] |~1 ) | int(message_binary[i])
        
    # reshaping array to its original form
    image_array = data_flatten.reshape(image_array.shape)
    
    # saving the encoded image
    encoded_image = Image.fromarray(image_array)
    encoded_image.save(out_image_path)
    print(f'Messae encoded and saved as {out_image_path}')
    
    
# Using an image
image_path ='picture.png'
message ="You will be hacked ne day unless you watch what is necessary"
out_image_path = "encoded_image.png"
encode_message(image_path, message, out_image_path)
