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
    image_opening = Image.open(image_path)
    image_opening = image_opening.convert("RGB")

    # Converting an image to numpy array
    image_array = np.array(image_opening)

    # converting the message into binary
    message_binary = (
                        ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'
                    ) 
    
    # checking if the image to assess it it can store the message accurtely
    if len(message_binary) > image_array.size*3:
        raise ValueError("Message is too long to hide in this image")
    
    #  flattemig the array to iterate over the image pixel
    data_flatten = image_array.flatten()
        
    # Encode the message in pixels
    for i in range(len(message_binary)):
        #  get the binary of the pixel
        data_flatten [i]= format(data_flatten[i] |~1 ) | int(message_binary)
        
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
