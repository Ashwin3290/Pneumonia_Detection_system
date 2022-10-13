import base64
import mysql.connector as myc
from datetime import datetime, timezone
import io
from PIL import Image
import numpy as np
import silence_tensorflow.auto
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from keras import regularizers
from tensorflow.keras.applications import ResNet50V2

conn=myc.connect(host='localhost',user='root',password='12345',database='pnuemonia')
cursor=conn.cursor()

base_model =ResNet50V2(weights='imagenet', input_shape=(224,224,3), include_top=False)
model=Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(512, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)),
    Dropout(0.5),
    Dense(128, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)),
    Dropout(0.3),
    Dense(64, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])
model.load_weights("saved_model/tuned_model")

def connect():
    global cursor,conn
    conn=myc.connect(host='localhost',user='root',password='12345',database='pnuemonia')
    cursor=conn.cursor()

def verify(token):
    connect()
    q="Select token_num from patient where token_num ="+str(token)
    cursor.execute(q)
    data=cursor.fetchall()
    conn.close()
    if not data:
        return True
    else:
        False

def display(data):
    connect()
    n=[]
    for row in data:
        d=[]
        for i in row:
            d.append(i)
        n.append(d)
    conn.close()
    if len(n)==1:
        return d
    else:
        return n


def add(name,token,date,loc,pred):
    q="Insert into patient values(%s,%s,%s,%s,%s);"
    blob=img_to_bin(loc)
    values=(name,str(token),str(date),blob,pred)
    connect()
    cursor.execute(q,values)
    conn.commit()
    conn.close()

def searchindata(name='',token=0):
    q="select * from patient where name=%s or token_num=%s"
    values=(name,str(token))
    connect()
    cursor.execute(q,values)    
    data=display(cursor.fetchall())
    if isinstance(data[0],list):
        for i in range(len(data)):
            data[i][3]=bin_to_img(data[i][3])
        return data,"multiple"
    else:
            data[3]=bin_to_img(data[3])
            return data,"single"

    
def predict(loc):
    img = Image.open(loc).resize((224,224))
    mode=img.mode
    if mode!="RGB":
        img=img.convert("RGB")
    x = np.asarray(img)
    x = np.expand_dims(x, axis=0)

    classes = model.predict(x, batch_size=10)
    if classes[0]>0.5:
        return "Normal"
    else:
        return "Pnuemonia"


def img_to_bin(loc):
    try:
        with open(loc,"rb") as file:
            binary=file.read()
            binary=base64.b64encode(binary)
        return binary
    except:
        print("problem with image")

def bin_to_img(binary):
    try:
        binary= base64.b64decode(binary)
        image = io.BytesIO(binary)
        return image
    except:
        print("Failed to create image")
