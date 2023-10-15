from fastapi import FastAPI, File, UploadFile, Request
from predict import proses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

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
        info = "Batik Megamendung berasal dari Cirebon, Jawa Barat. Motifnya berupa awan mendung yang digambarkan dengan gradasi warna. Filosofi batik Megamendung adalah kehidupan yang penuh perubahan, sedangkan maknanya adalah keabadian cinta dan kasih sayang."
        image = "assets\img\Megamendung.jpg"
    elif label == "Kawung":
        info = "Batik Kawung berasal dari Jawa Tengah. Motifnya berupa buah kawung yang digambarkan dengan pola geometris. Filosofi batik Kawung adalah kekuasaan dan kemakmuran, sedangkan maknanya adalah keberhasilan dan kemakmuran."
        image = "assets\img\Kawung.jfif"
    elif label == "Parang":
        info = "Batik Parang berasal dari Solo, Jawa Tengah. Motifnya berupa ombak laut yang digambarkan dengan pola geometris. Filosofi batik Parang adalah kekuatan dan keabadian, sedangkan maknanya adalah semangat perjuangan dan pantang menyerah."
        image = "assets\img\Parang.jpg"
    elif label == "Sekarjagad":
        info = "Batik Sekar Jagad berasal dari Yogyakarta. Motifnya berupa alam semesta yang digambarkan dengan berbagai macam flora dan fauna. Filosofi batik Sekar Jagad adalah keharmonisan dan keseimbangan alam, sedangkan maknanya adalah keindahan dan keajaiban alam semesta."
        image = "assets\img\Sekarjagad.jpg"
    elif label == "Truntum":
        info = "Batik Truntum berasal dari Yogyakarta. Motifnya berupa bunga truntum yang digambarkan dengan pola geometris. Filosofi batik Truntum adalah kesuburan dan kemakmuran, sedangkan maknanya adalah kebahagiaan dan cinta."
        image = "assets\img\Truntum.jpg"
    
    hasil = label + " ("+str(f"{conf*100:.2f}") + "%)" + "\n\n" + info + "\n\n"

    return {"Text": hasil, "Image": image, "Label": label}


# python -m uvicorn predictCV:app --reload
if __name__ == '__main__':
    # nanti di cloud run samain juga CONTAINER PORT -> 3000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000))) 