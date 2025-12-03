from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Import from same package
from .algorithm import encrypt, decrypt

app = FastAPI()

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Serve favicon files from root
@app.get("/favicon.ico")
async def get_favicon():
    favicon_path = os.path.join(BASE_DIR, "favicon.ico")
    return FileResponse(favicon_path)

@app.get("/apple-touch-icon.png")
async def get_apple_touch_icon():
    icon_path = os.path.join(BASE_DIR, "apple-touch-icon.png")
    return FileResponse(icon_path)

@app.get("/favicon-16x16.png")
async def get_favicon_16():
    icon_path = os.path.join(BASE_DIR, "favicon-16x16.png")
    return FileResponse(icon_path)

@app.get("/favicon-32x32.png")
async def get_favicon_32():
    icon_path = os.path.join(BASE_DIR, "favicon-32x32.png")
    return FileResponse(icon_path)

@app.get("/site.webmanifest")
async def get_manifest():
    manifest_path = os.path.join(BASE_DIR, "site.webmanifest")
    return FileResponse(manifest_path)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, text: str = Form(...), mode: str = Form(...)):
    if mode == "encrypt":
        output = encrypt(text)
    else:
        output = decrypt(text)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "input": text,
        "output": output,
        "mode": mode
    })

@app.get("/api/health")
async def health():
    return {"status": "ok"}