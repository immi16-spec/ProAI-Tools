import streamlit as st
import onnxruntime as ort
from rembg import remove

# Force verification: check if onnxruntime is loaded
try:
    providers = ort.get_available_providers()
    st.write(f"ONNX Runtime loaded with providers: {providers}")
except Exception as e:
    st.error("ONNX Runtime load nahi hua! " + str(e))
