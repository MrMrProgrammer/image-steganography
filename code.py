from PIL import Image
import numpy as np

def hide_image_fixed(cover_path, secret_path, output_path):
    cover = Image.open(cover_path).convert('RGB')
    secret = Image.open(secret_path).convert('L')  # grayscale

    # Resize secret
    secret = secret.resize(cover.size)

    # Convert to numpy arrays
    cover_arr = np.array(cover, dtype=np.uint8)
    secret_arr = np.array(secret, dtype=np.uint8)

    # Threshold secret: black text=1, white background=0
    secret_arr = (secret_arr < 128).astype(np.uint8)  # black text=1

    # Hide in LSB of red channel
    stego_arr = cover_arr & 0b11111110
    stego_arr[:, :, 0] |= secret_arr

    Image.fromarray(stego_arr).save(output_path)
    print(f"Secret hidden in {output_path}")

def extract_hidden_image(stego_path, output_path):
    stego = Image.open(stego_path).convert('RGB')
    arr = np.array(stego, dtype=np.uint8)

    secret_bits = arr[:, :, 0] & 1
    secret_img = (1 - secret_bits) * 255
    Image.fromarray(secret_img.astype(np.uint8)).save(output_path)
    print(f"Hidden image extracted as {output_path}")

# Usage
hide_image_fixed('cover.jpg', 'secret.png', 'stego.png')
extract_hidden_image('stego.png', 'hidden_fixed.png')
