# to work with image, PIL module is need
import itertools
import keylogger
from PIL import Image

# converting text to binary
def text_to_binary(text):
    # ord(a) get the ASCII value of the character 'a'
    # format(ord(a), '08b') helps in ASCIIIvalue to an 8-bit binary string 
    # the join() concatenate all these binary stirngs to form a single binay
    return ''.join(format(ord(a), '08b') for a in text)

# converting binary to text
def binary_to_text(binary):
    # binary[a:a+8] slice the binary string into 8 bits which is equivalent to 1byte 
    # chr(int(binary[a:a+8], 2)) convert the binary string to ASCII value
    # join() concatenate all these ASCII values to form anoriginal string
    binary_values = [binary[a:a+8] for a in range(0, len(binary), 8)]
    return ''. join(chr(int(bv,2)) for bv in binary_values)


# Embedding Text int an Image
def embed_text(image_path, ouput_image_path, text):
    image_path = 'embed.png'
    image = Image.open(image_path)

    binary_text = f"{text_to_binary(text)}1111111111111110"
    data_index = 0

    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            if data_index < len(binary_text):
                pixel = list(pixels[x,y])
                for n in range(3):
                    if data_index < len(binary_text):
                        pixel[n] = int(format(pixel[n], '08b')[:-1] +binary_text[data_index], 2)
                        data_index +=1
                pixels[x, y] = tuple(pixel)
            else:
                break
    image.save(ouput_image_path)
    
# extracting text from the image
def extract_text(image_path):
    image = Image.open(image_path)
    binary_data = ""

    pixels = image.load()

    for y, x in itertools.product(range(image.height), range(image.width)):
        pixel = pixels[x,y]
        for n in range(3):
            binary_data += format(pixel[n], '08b')[-1]

    delimiter_index = binary_data.find('1111111111111110')
    binary_data = binary_data[:delimiter_index]

    return binary_to_text(binary_data)


if __name__ == "__main__":
    code = keylogger # imported module from the code
    
    embed_text('input_image.png', 'output_image.png', code)
    extracted_code = extract_text('output_image.png')
    
    print("Extracted Code:")
    print(extracted_code)
            