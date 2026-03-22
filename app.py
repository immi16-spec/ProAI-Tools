import streamlit as st
from rembg import remove
from PIL import Image
import io
import yt_dlp

st.title("ProAI Tools")

tab1, tab2 = st.tabs(["Thumbnail Downloader", "BG Remover"])

with tab1:
    url = st.text_input("YouTube URL:")
    if st.button("Get Thumbnail"):
        vid = url.split("v=")[-1].split("&")[0]
        st.image(f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg")

with tab2:
    file = st.file_uploader("Upload Image", type=['png', 'jpg'])
    if file:
        input_image = file.read()
        output = remove(input_image) # Ab ye chalega!
        st.image(output)
        st.download_button("Download", output, "bg_removed.png")
