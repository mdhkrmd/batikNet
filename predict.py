from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input
import numpy as np
import keras
from keras.models import load_model

def proses(file):
    model_baru=load_model('effNetV2.h5')
    jenis = ['Kawung', 'Megamendung', 'Parang', 'Sekarjagad', 'Truntum']

    image = Image.open(file.file)
    image = preprocess_input(image)
    image = image.convert('RGB')
    image = image.resize((224,224))
    image = np.asarray(image)
    image = np.expand_dims(image,0)
    # image = image/255.0
    
    p = model_baru.predict(image)
    kelas = p.argmax(axis = 1)[0]
    label = jenis[kelas]
    conf = p[0][kelas]
    return conf, label