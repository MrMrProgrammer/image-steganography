import streamlit as st
import numpy as np
from PIL import Image


# -----------------------------------------------------------------------------
# Extract 8 bit-planes from RED channel
# -----------------------------------------------------------------------------
def extract_bit_planes_rgb(img):
    img = img.convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    R = arr[:, :, 0]

    planes = []
    for bit in range(8):
        plane = ((R >> bit) & 1) * 255
        planes.append(Image.fromarray(plane.astype(np.uint8)))
    return planes


# -----------------------------------------------------------------------------
# Hide secret inside LSB of RED channel
# -----------------------------------------------------------------------------
def hide_lsb_rgb(cover_img, secret_img):
    cover = cover_img.convert("RGB")
    secret = secret_img.convert("L").resize(cover.size)

    cover_arr = np.array(cover, dtype=np.uint8)
    secret_arr = np.array(secret, dtype=np.uint8)

    secret_bit = (secret_arr > 128).astype(np.uint8)

    stego_arr = cover_arr.copy()
    stego_arr[:, :, 0] = (cover_arr[:, :, 0] & 0b11111110) | secret_bit

    return Image.fromarray(stego_arr.astype(np.uint8))


# -----------------------------------------------------------------------------
# Extract (Recovered Cover + Secret)
# -----------------------------------------------------------------------------
def extract_from_stego(stego_img):
    stego_arr = np.array(stego_img.convert("RGB"), dtype=np.uint8)

    # Extract LSB as secret
    secret_bits = (stego_arr[:, :, 0] & 1)
    secret_img = Image.fromarray((secret_bits * 255).astype(np.uint8))

    # Recover cover (remove secret bit)
    recovered = stego_arr.copy()
    recovered[:, :, 0] &= 0b11111110
    recovered_cover = Image.fromarray(recovered.astype(np.uint8))

    return recovered_cover, secret_img


# -----------------------------------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------------------------------

st.markdown(
    "<p style='font-size:30px;'>RGB LSB Image Steganography 🎨<br>"
    "Bit-Plane Viewer 🔍<br></p>"
    "<p style='font-size:20px;'>LSB = Least Significant Bit</p>",
    unsafe_allow_html=True
)

mode = st.radio(
    "Select mode:",
    [
        "View Bit-Planes",
        "Hide Secret (Cover + Secret → Stego)",
        "Extract from Stego (Stego → Cover + Secret)"
    ]
)

# -----------------------------------------------------------------------------
# MODE 1 — View Bit Planes
# -----------------------------------------------------------------------------
if mode == "View Bit-Planes":
    st.header("Upload an Image to View Its 8 Bit-Planes 📸")
    file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"]
    )

    if file:
        img = Image.open(file)
        st.image(img, caption="Input Image", width="stretch")

        st.subheader("Red Channel Bit Planes")
        planes = extract_bit_planes_rgb(img)

        cols = st.columns(4)
        for i in range(8):
            with cols[i % 4]:
                st.image(planes[i], caption=f"Bit {i}", width="stretch")


# -----------------------------------------------------------------------------
# MODE 2 — Hide Secret
# -----------------------------------------------------------------------------
elif mode == "Hide Secret (Cover + Secret → Stego)":

    st.header("Upload Cover Image")
    cover_file = st.file_uploader(
        "Upload Cover Image",
        type=["png", "jpg", "jpeg"],
        key="cover"
    )

    st.header("Upload Secret Image")
    secret_file = st.file_uploader(
        "Upload Secret Image",
        type=["png", "jpg", "jpeg"],
        key="secret"
    )

    if cover_file and secret_file:
        cover = Image.open(cover_file)
        secret = Image.open(secret_file)

        st.subheader("Cover Image")
        st.image(cover, width="stretch")

        st.subheader("Secret Image")
        st.image(secret, width="stretch")

        # ------------------ Stego ------------------
        stego = hide_lsb_rgb(cover, secret)

        st.header("Stego Image")
        st.image(stego, width="stretch")

        stego.save("stego_output.png")
        st.download_button(
            "Download Stego Image",
            open("stego_output.png", "rb"),
            file_name="stego.png"
        )

        # ------------------ Bit Planes ------------------
        st.subheader("Stego Bit-Planes")
        planes = extract_bit_planes_rgb(stego)

        cols = st.columns(4)
        for i in range(8):
            with cols[i % 4]:
                st.image(planes[i], caption=f"Bit {i}", width="stretch")


# -----------------------------------------------------------------------------
# MODE 3 — Extract from Stego
# -----------------------------------------------------------------------------
elif mode == "Extract from Stego (Stego → Cover + Secret)":

    st.header("Upload Stego Image")
    stego_file = st.file_uploader(
        "Upload Stego Image",
        type=["png", "jpg", "jpeg"],
        key="stego"
    )

    if stego_file:
        stego = Image.open(stego_file)

        st.subheader("Stego Image")
        st.image(stego, width="stretch")

        # -------- extraction --------
        recovered_cover, extracted_secret = extract_from_stego(stego)

        st.header("Recovered Cover")
        st.image(recovered_cover, width="stretch")

        st.header("Extracted Secret Image")
        st.image(extracted_secret, width="stretch")

        recovered_cover.save("recovered_cover.png")
        extracted_secret.save("extracted_secret.png")

        st.download_button(
            "Download Recovered Cover",
            open("recovered_cover.png", "rb"),
            file_name="cover.png"
        )
        st.download_button(
            "Download Secret Image",
            open("extracted_secret.png", "rb"),
            file_name="secret.png"
        )

        # ------------------ Bit Planes ------------------
        st.subheader("Stego Bit-Planes")
        planes = extract_bit_planes_rgb(stego)

        cols = st.columns(4)
        for i in range(8):
            with cols[i % 4]:
                st.image(planes[i], caption=f"Bit {i}", width="stretch")

# -----------------------------------------------------------------------------
