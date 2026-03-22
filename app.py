import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import yt_dlp
import requests

# Page Config
st.set_page_config(page_title="ProAI Tools", layout="wide")

st.title("🚀 ProAI Tools - Thumbnail & BG Remover")

# Tabs
tab1, tab2, tab3 = st.tabs(["Thumbnail Downloader", "BG Remover", "Video Downloader"])

with tab1:
    st.header("YouTube Thumbnail Downloader")
    url = st.text_input("Paste YouTube URL:")
    if st.button("Get Thumbnails"):
        try:
            vid = url.split("v=")[-1].split("&")[0]
            if "youtu.be/" in url: vid = url.split("youtu.be/")[1].split("?")[0]
            
            cols = st.columns(4)
            sizes = ["maxresdefault", "sddefault", "hqdefault", "mqdefault"]
            for i, size in enumerate(sizes):
                img_url = f"https://img.youtube.com/vi/{vid}/{size}.jpg"
                cols[i].image(img_url)
                cols[i].markdown(f"[Download {size}]({img_url})")
        except: st.error("Invalid URL!")

with tab2:
    st.header("AI Background Remover")
    file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if file:
        input_image = file.read()
        try:
            # Safe Rembg load
            output = remove(input_image)
            st.image(output, caption="Background Removed")
            st.download_button("Download PNG", output, "bg_removed.png", "image/png")
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.header("Video Downloader")
    v_url = st.text_input("Paste Video URL")
    if st.button("Download Video"):
        try:
            ydl_opts = {'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([v_url])
            with open("video.mp4", "rb") as f:
                st.download_button("Save Video", f, "video.mp4")
        except Exception as e:
            st.error(f"Error: {e}")
