from fastapi import FastAPI, File, UploadFile, Request, HTTPException
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
import mysql.connector
import time
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

# Load your model
model_baru=load_model('effNetV2.h5')
jenis = ['Kawung', 'Megamendung', 'Parang', 'Sekarjagad', 'Truntum']


def video_feed_generator() -> Generator[bytes, None, None]:
    # OpenCV VideoCapture
    cap = cv2.VideoCapture(0)
    upload_interval = 2  # Set the upload interval in seconds
    last_upload_time = time.time()

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

        if np.sum(y) == 1:
            kelas = np.argmax(y)
            label = jenis[kelas]

            # Get the probability for the predicted class
            probabilitas = y[0][kelas]
            if probabilitas >= 0.7:
                teks = f'{label} - Probabilitas: {probabilitas:.2f}'
                cv2.putText(gbr1, teks, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Save the image locally
                save_path = 'saved_pictures_video'
                os.makedirs(save_path, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                image_filename = f'{timestamp}_{label}_prob_{probabilitas:.2f}.jpg'
                image_path = os.path.join(save_path, image_filename)
                cv2.imwrite(image_path, gbr1)
                print(f'Image saved: {image_path}')
                
                # Upload ke database
                current_time = time.time()
                if current_time - last_upload_time >= upload_interval:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="batikclf"
                    )

                    mycursor = mydb.cursor()

                    sql = "INSERT INTO predictvideo (label, conf) VALUES  (%s, %s)"
                    val = (label, float(probabilitas))
                    mycursor.execute(sql, val)

                    mydb.commit()

                    print(mycursor.rowcount, "record inserted.")

                    last_upload_time = current_time

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
        info = "Megamendung batik comes from Cirebon, West Java. The pattern is cloudy clouds depicted with color gradations. The philosophy of Megamendung batik is a life entirely of change, while its meaning is the eternity of love and affection."
        image = "assets\img\Megamendung.jpg"
    elif label == "Kawung":
        info = "Kawung batik comes from Central Java. The pattern is a kawung fruit depicted in a geometric pattern. The philosophy of Kawung batik is power and prosperity, while its meaning is success and prosperity."
        image = "assets\img\Kawung.jfif"
    elif label == "Parang":
        info = "Parang Batik comes from Solo, Central Java. The pattern is sea waves depicted in geometric patterns. The philosophy of Parang batik is strength and eternity, while its meaning is the spirit of struggle and never giving up."
        image = "assets\img\Parang.jpg"
    elif label == "Sekarjagad":
        info = "Batik Sekar Jagad comes from Yogyakarta. The pattern is the universe depicted with various kinds of flora and fauna. The philosophy of Sekar Jagad batik is harmony and balance of nature, while its meaning is the beauty and wonder of the universe."
        image = "assets\img\Sekarjagad.jpg"
    elif label == "Truntum":
        info = "Truntum batik comes from Yogyakarta. The pattern is a truntum flower depicted in a geometric pattern. The philosophy of Truntum batik is fertility and prosperity, while its meaning is happiness and love."
        image = "assets\img\Truntum.jpg"
    
    hasil = label + " ("+str(f"{conf*100:.2f}") + "%)" + "\n\n" + info + "\n\n"

    return {"Text": hasil, "Image": image, "Label": label}

# python -m uvicorn predictCV:app --reload
if __name__ == '__main__':
    # nanti di cloud run samain juga CONTAINER PORT -> 3000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000))) 
    
# ================================
# class DataPayload(BaseModel):
#     label: str
#     probability: float

# @app.post("/upload_to_database")
# async def upload_to_database(data: DataPayload):
#     label = data.label
#     probability = data.probability

#     cap = cv2.VideoCapture(0)
#     _, gbr1 = cap.read()
#     save_path = 'saved_pictures_video'
#     os.makedirs(save_path, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     image_filename = f'{timestamp}_{label}_prob_{probability:.2f}.jpg'
#     image_path = os.path.join(save_path, image_filename)
#     cv2.imwrite(image_path, gbr1)
#     print(f'Image saved: {image_path}')
    
#     mydb = mysql.connector.connect(
#                         host="localhost",
#                         user="root",
#                         password="",
#                         database="batikclf"
#                     )

#     mycursor = mydb.cursor()

#     sql = "INSERT INTO predictvideo (label, conf) VALUES  (%s, %s)"
#     val = (label, float(probability))
#     mycursor.execute(sql, val)

#     mydb.commit()

#     print(mycursor.rowcount, "record inserted.")

#     return {"status": "success"}