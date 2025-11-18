from PIL import Image
import numpy as np
import os

def extract_from_stego(stego_path, output_folder='output'):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load stego image
    stego = Image.open(stego_path).convert('RGB')
    stego_arr = np.array(stego, dtype=np.uint8)

    # ----------------- Extract secret -----------------
    secret_bits = stego_arr[:, :, 0] & 1
    secret_img = (1 - secret_bits) * 255  # black text = 1
    secret_path = os.path.join(output_folder, 'secret_extracted.png')
    Image.fromarray(secret_img.astype(np.uint8)).save(secret_path)

    # ----------------- Recover approximate cover -----------------
    recovered_cover_arr = stego_arr.copy()
    recovered_cover_arr[:, :, 0] &= 0b11111110  # zero out LSB
    cover_path = os.path.join(output_folder, 'cover_recovered.png')
    Image.fromarray(recovered_cover_arr).save(cover_path)

    print(f"Secret image saved as '{secret_path}'")
    print(f"Recovered cover image saved as '{cover_path}'")

# ----------------- USAGE -----------------
# extract_from_stego('stego.png')
extract_from_stego('cover.jpg')
