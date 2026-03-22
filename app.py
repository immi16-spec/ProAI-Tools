import streamlit as st
import requests
from PIL import Image
from rembg import remove
from io import BytesIO
import yt_dlp

st.set_page_config(layout="wide")
st.title("ProAI Tools")

tab1, tab2, tab3, tab4 = st.tabs(["Thumbnail Downloader", "BG Remover", "Video Downloader", "Image Compressor"])

with tab1:
    url = st.text_input("Enter YouTube URL")
    if st.button("Get Thumbnails"):
        vid = url.split("v=")[-1].split("&")[0]
        st.image(f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg")

with tab2:
    file = st.file_uploader("Upload Image", type=['png', 'jpg'])
    if file:
        input_image = file.read()
        output = remove(input_image)
        st.image(output)
        st.download_button("Download", output, "bg_removed.png")

with tab3:
    v_url = st.text_input("Paste Video URL")
    if st.button("Download Video"):
        ydl_opts = {'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
        with open("video.mp4", "rb") as f:
            st.download_button("Save Video", f, "video.mp4")

with tab4:
    img_file = st.file_uploader("Upload for Compressor", type=['jpg', 'png'])
    if img_file:
        img = Image.open(img_file)
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=50)
        st.download_button("Download Compressed", buf.getvalue(), "image.webp")
