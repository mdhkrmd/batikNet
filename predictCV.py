from fastapi import FastAPI, File, UploadFile, Request
from predict import proses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import  StreamingResponse
import uvicorn
import os
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from typing import Generator
from PIL import Image
import keras
from tensorflow.keras.applications.efficientnet import preprocess_input

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

# Load your model
model_baru=load_model('effNetV2.h5')
jenis = ['Kawung', 'Megamendung', 'Parang', 'Sekarjagad', 'Truntum']

# OpenCV VideoCapture
cap = cv2.VideoCapture(0)

def video_feed_generator() -> Generator[bytes, None, None]:
    while True:
        _, gbr1 = cap.read()
        gbr2 = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr2)

        width, height = gbr.size
        left = np.round((width - height) / 2)
        right = left + height
        gbr = gbr.crop((left, 0, right, height))
        img = gbr.resize((224, 224))

        img = np.expand_dims(img, axis=0)
        gambar = preprocess_input(img)

        y = model_baru.predict(gambar, verbose=0)
        y = np.round(y)

        if np.sum(y) == 1:
            kelas = np.where(y[0] == 1)
            cv2.putText(gbr1, jenis[kelas[0][0]], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        _, buffer = cv2.imencode('.jpg', gbr1)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index-2.html", {"request": request})

@app.get("/old")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/video_feed")
async def video_feed_endpoint():
    return StreamingResponse(video_feed_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

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