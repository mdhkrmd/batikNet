from fastapi import FastAPI, File, UploadFile, Request
from predict import proses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# python -m uvicorn predictCV:app --reload

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index-2.html", {"request": request})

@app.get("/old")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/prediksi")
async def predict_image(file: UploadFile = File(...)):
    conf, label = proses(file)
    hasil = label + " ("+str(f"{conf*100:.2f}") + "%)"
    
    return {"Text":hasil}

# python -m uvicorn predictCV:app --reload
if __name__ == '__main__':
    # nanti di cloud run samain juga CONTAINER PORT -> 3000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000))) 