import streamlit as st
from PIL import Image
import numpy as np
import os

# ----------------- CORE FUNCTIONS -----------------
def hide_image(cover_img, secret_img):
    cover = cover_img.convert('RGB')
    secret = secret_img.convert('L').resize(cover.size)

    cover_arr = np.array(cover, dtype=np.uint8)
    secret_arr = np.array(secret, dtype=np.uint8)

    secret_arr = (secret_arr < 128).astype(np.uint8)  # black text = 1
    stego_arr = cover_arr.copy()
    stego_arr[:, :, 0] = (cover_arr[:, :, 0] & 0b11111110) | secret_arr

    stego_img = Image.fromarray(stego_arr)
    return stego_img

def extract_from_stego(stego_img):
    stego_arr = np.array(stego_img.convert('RGB'), dtype=np.uint8)

    secret_bits = stego_arr[:, :, 0] & 1
    secret_img = Image.fromarray(((1 - secret_bits) * 255).astype(np.uint8))

    recovered_cover_arr = stego_arr.copy()
    recovered_cover_arr[:, :, 0] &= 0b11111110
    recovered_cover_img = Image.fromarray(recovered_cover_arr)

    return recovered_cover_img, secret_img

# ----------------- STREAMLIT FRONTEND -----------------
st.title("LSB Image Steganography")

option = st.radio("Choose operation:", ["Hide Secret", "Extract Secret"])

if option == "Hide Secret":
    cover_file = st.file_uploader("Upload cover image", type=["png","jpg","jpeg"])
    secret_file = st.file_uploader("Upload secret image (black & white)", type=["png","jpg","jpeg"])

    if cover_file and secret_file:
        cover_img = Image.open(cover_file)
        secret_img = Image.open(secret_file)

        stego_img = hide_image(cover_img, secret_img)

        st.image(stego_img, caption="Stego Image", use_column_width=True)

        # Provide download
        stego_img.save("stego.png")
        st.download_button("Download Stego Image", data=open("stego.png","rb"), file_name="stego.png")

elif option == "Extract Secret":
    stego_file = st.file_uploader("Upload stego image", type=["png","jpg","jpeg"])

    if stego_file:
        stego_img = Image.open(stego_file)
        recovered_cover_img, secret_img = extract_from_stego(stego_img)

        st.subheader("Recovered Cover")
        st.image(recovered_cover_img, use_column_width=True)

        st.subheader("Extracted Secret")
        st.image(secret_img, use_column_width=True)

        # Save for download
        recovered_cover_img.save("cover_recovered.png")
        secret_img.save("secret_extracted.png")

        st.download_button("Download Recovered Cover", data=open("cover_recovered.png","rb"), file_name="cover_recovered.png")
        st.download_button("Download Secret Image", data=open("secret_extracted.png","rb"), file_name="secret_extracted.png")
