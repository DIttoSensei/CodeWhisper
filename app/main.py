from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.algorithm import encrypt, decrypt

app = FastAPI()
templates = Jinja2Templates(directory="static")


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
