from PIL import Image
import numpy as np

# ----------------- HIDE IMAGE -----------------
def hide_image(cover_path, secret_path, stego_path):
    """
    Hides a black-and-white secret image inside a cover image using LSB.
    """
    # Load cover and secret
    cover = Image.open(cover_path).convert('RGB')
    secret = Image.open(secret_path).convert('L')  # grayscale

    # Resize secret to match cover
    secret = secret.resize(cover.size)

    # Convert to numpy arrays
    cover_arr = np.array(cover, dtype=np.uint8)
    secret_arr = np.array(secret, dtype=np.uint8)

    # Threshold secret: black text=1, white background=0
    secret_arr = (secret_arr < 128).astype(np.uint8)

    # Hide secret in LSB of red channel
    stego_arr = cover_arr.copy()
    stego_arr[:, :, 0] = (cover_arr[:, :, 0] & 0b11111110) | secret_arr

    # Save stego image
    Image.fromarray(stego_arr).save(stego_path)
    print(f"Stego image saved as '{stego_path}'")

# ----------------- EXTRACT IMAGES -----------------
def extract_images(stego_path, recovered_cover_path, secret_path):
    """
    Extracts the hidden secret image and an approximation of the original cover image
    from a stego image.
    """
    stego = Image.open(stego_path).convert('RGB')
    stego_arr = np.array(stego, dtype=np.uint8)

    # Extract secret from LSB of red channel
    secret_bits = stego_arr[:, :, 0] & 1
    secret_img = (1 - secret_bits) * 255  # black text=1
    Image.fromarray(secret_img.astype(np.uint8)).save(secret_path)

    # Recover approximate cover by zeroing LSB
    recovered_cover_arr = stego_arr.copy()
    recovered_cover_arr[:, :, 0] &= 0b11111110  # zero out LSB
    Image.fromarray(recovered_cover_arr).save(recovered_cover_path)

    print(f"Secret image saved as '{secret_path}'")
    print(f"Recovered cover image saved as '{recovered_cover_path}'")

# ----------------- USAGE EXAMPLE -----------------
# Hide secret
hide_image('cover.jpg', 'secret.png', 'stego.png')

# Extract both images
# extract_images('stego.png', 'cover_recovered.png', 'secret_extracted.png')
