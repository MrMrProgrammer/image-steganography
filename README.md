# 🖼️ Image Steganography (LSB) + Bit-Plane Viewer

Hide & extract secret images using Least Significant Bit (LSB)
steganography

🚀 **Live Demo:**\
https://huggingface.co/spaces/MrMrProgrammer/ImageSteganography

📂 **GitHub Repository:**\
https://github.com/MrMrProgrammer/image-steganography

------------------------------------------------------------------------

## 📌 Overview

This project demonstrates **image steganography** using the **LSB (Least
Significant Bit)** technique.\
LSB Steganography lets you hide a secret image *inside* another image
--- in a way that is invisible to the human eye.

Additionally, the app includes a **Bit-Plane Viewer**, allowing you to
visually inspect all 8 bit-layers of an image and better understand how
digital images store information.

This tool is ideal for:
- 🧪 Students learning steganography
- 🔍 Security & forensics demos
- 🎨 Curiosity about how images store data
- 🧠 Research experiments

------------------------------------------------------------------------

## ✨ Features

### 🔹 1. View Bit-Planes

Upload any image and see its **8 binary layers** (Bit 0 to Bit 7).\
This helps visualize how modifying only the least significant bit barely
affects the appearance.

------------------------------------------------------------------------

### 🔹 2. Hide Secret Image

Upload:
- A **Cover Image**
- A **Secret Image**

The app hides the secret inside the cover using the **red-channel LSB**,
producing a new **Stego Image**.

You can:
- Preview the stego image
- Download it
- View its bit-planes

------------------------------------------------------------------------

### 🔹 3. Extract From Stego

Upload a stego image and automatically extract:
- 🟦 The recovered cover image
- 🟨 The extracted secret image

Both reconstructed images can be downloaded.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python 3**
-   **Streamlit**
-   **NumPy**
-   **Pillow (PIL)**

------------------------------------------------------------------------

## 📥 Installation

Clone the repo:

``` bash
git clone https://github.com/MrMrProgrammer/image-steganography
cd image-steganography
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the app:

``` bash
streamlit run src/streamlit_app.py
```

------------------------------------------------------------------------

## 📌 How LSB Steganography Works (Brief)

Every pixel in an RGB image has values like:

    R: 11001010  
    G: 10101001  
    B: 11110000

If we replace **only the last bit** (LSB):

    1100101[0] → 1100101[1]

The human eye **cannot see this tiny change**, but software can ---
meaning we can hide binary data inside the image.

This project hides the secret image's **binary threshold** into the LSB
of the **Red channel**.

------------------------------------------------------------------------

## 📄 File Structure

    📁 image-steganography
    │── src/
    │     └── streamlit_app.py
    │── requirements.txt
    │── README.md
    │── Dockerfile
    │── .gitattributes

------------------------------------------------------------------------

## 🌐 Online Deployment

This app is deployed for free on **HuggingFace Spaces** using Streamlit.

------------------------------------------------------------------------

## ⭐ Support

If this project was useful to you, please consider:

🌟 Starring the repo on GitHub\
🔄 Sharing it on LinkedIn\
📥 Giving feedback or suggestions

------------------------------------------------------------------------

## 📧 Contact

Created by **MrMrProgrammer**