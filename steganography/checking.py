# This program will hide a message in an image using the least significant bits of the pixels

from PIL import Image
import numpy as np

# A function to encode the message 
def encode_message(image_path, message, out_image_path):
    # Open the image
    image_opening = Image.open(image_path)
    image_opening = image_opening.convert("RGB")

    # Converting an image to numpy array
    image_array = np.array(image_opening)

    # Converting the message into binary
    message_binary = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'  # Delimiter to mark the end
    
    # Checking if the image can store the message accurately
    if len(message_binary) > image_array.size * 3:
        raise ValueError("Message is too long to hide in this image")
    
    # Flattening the array to iterate over the image pixels
    data_flatten = image_array.flatten()
        
    # Encode the message in the least significant bit of the pixels
    for i in range(len(message_binary)):
        # Modify the LSB of the pixel value
        data_flatten[i] = (data_flatten[i] & ~1) | int(message_binary[i])
        
    # Reshaping array to its original form
    image_array = data_flatten.reshape(image_array.shape)
    
    # Saving the encoded image
    encoded_image = Image.fromarray(image_array)
    encoded_image.save(out_image_path)
    print(f'Message encoded and saved as {out_image_path}')
    
# Using an image
image_path = 'C:\\Users\\Admin Pc\\Desktop\\project_60\\picture.png'  # Correct path to your image
message = "You will be hacked one day unless you watch what is necessary"
out_image_path = 'C:\\Users\\Admin Pc\\Desktop\\project_60\\encoded_image.png'  # Output path for the encoded image

# Encode the message
encode_message(image_path, message, out_image_path)
