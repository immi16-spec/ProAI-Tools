from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates
from rembg import remove
from io import BytesIO
from PIL import Image
import requests
import yt_dlp
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request): return templates.TemplateResponse("index.html", {"request": request})

@app.get("/upscaler", response_class=HTMLResponse)
async def upscaler_page(request: Request): return templates.TemplateResponse("upscaler.html", {"request": request})

@app.get("/download-thumb")
async def download_thumb(url: str):
    res = requests.get(url)
    return Response(content=res.content, media_type="image/jpeg")

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    output_image = remove(input_image)
    return StreamingResponse(BytesIO(output_image), media_type="image/png")

@app.post("/upscale-image")
async def upscale_img(file: UploadFile = File(...), scale: int = Form(2)):
    input_image = await file.read()
    img = Image.open(BytesIO(input_image))
    if scale > 8: scale = 8
    new_size = (int(img.width * scale), int(img.height * scale))
    upscaled_img = img.resize(new_size, Image.Resampling.LANCZOS)
    img_io = BytesIO()
    save_format = img.format if img.format else "PNG"
    upscaled_img.save(img_io, format=save_format)
    img_io.seek(0)
    return StreamingResponse(img_io, media_type=f"image/{save_format.lower()}")