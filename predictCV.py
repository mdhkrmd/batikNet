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
    if label == "Megamendung":
        info = "Megamendung is a batik motif with a cloud pattern that originates from Cirebon"
        image = "assets\img\Megamendung.jpg"
    elif label == "Kawung":
        info = "Batik Kawung originates from Yogyakarta. It is known to have a high philosophical value and is not only applied to cloth or clothing."
        image = "assets\img\Kawung.jfif"
    elif label == "Parang":
        info = "Batik Parang is one of the oldest Indonesian batik motifs. It was worn by kings, leaders, and knights during the keraton Mataram Kartasura era in the 1600s."
        image = "assets\img\Parang.jpg"
    elif label == "Sekarjagad":
        info = "The Sekar Jagad batik motif symbolizes all the diversity that exists in Indonesia and the world. It was developed in the 18th century."
        image = "assets\img\Sekarjagad.jpg"
    elif label == "Truntum":
        info = "Truntum is a batik motif that symbolizes growth. This motif, which originates from the Surakarta Sunanate, has a long history in the formation of this truntum motif."
        image = "assets\img\Truntum.jpg"
    
    hasil = label + " ("+str(f"{conf*100:.2f}") + "%)" + "\n\n" + info + "\n\n"

    return {"Text": hasil, "Image": image, "Label": label}


# python -m uvicorn predictCV:app --reload
if __name__ == '__main__':
    # nanti di cloud run samain juga CONTAINER PORT -> 3000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000))) 