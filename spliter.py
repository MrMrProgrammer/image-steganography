# from PIL import Image
# import numpy as np

# def extract_secret_image(stego_path, output_path):
#     """
#     Extracts a hidden black-and-white image from the LSB of the red channel.
#     """
#     # Open stego image
#     stego = Image.open(stego_path).convert('RGB')
#     arr = np.array(stego, dtype=np.uint8)

#     # Extract the LSB from red channel
#     secret_bits = arr[:, :, 0] & 1

#     # Convert to black-and-white image (0=white, 1=black)
#     secret_img = (1 - secret_bits) * 255

#     # Save extracted secret
#     Image.fromarray(secret_img.astype(np.uint8)).save(output_path)
#     print(f"Secret image extracted and saved as '{output_path}'")

# # ------------------- USAGE -------------------
# extract_secret_image('stego.png', 'secret_extracted.png')


from PIL import Image
import numpy as np
import os

def save_bit_layers(image_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img, dtype=np.uint8)

    channels = ['red', 'green', 'blue']

    # Loop over each channel
    for c_idx, c_name in enumerate(channels):
        channel = arr[:, :, c_idx]

        # Loop over each bit (0 = LSB, 7 = MSB)
        for bit in range(8):
            # Extract the bit
            bit_layer = (channel >> bit) & 1
            # Scale to 0-255 for visualization
            bit_layer_img = (bit_layer * 255).astype(np.uint8)
            # Save image
            filename = os.path.join(output_folder, f'{c_name}_bit{bit}.png')
            Image.fromarray(bit_layer_img).save(filename)

    print(f"All 8-bit layers saved in '{output_folder}'")

# ----------------- USAGE -----------------
save_bit_layers('stego.png', 'bit_layers')
