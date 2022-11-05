import os
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2
from skimage.morphology import disk
import tensorflow_hub as hub
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

class Predictor:
    def __init__(self, labels_path: str, model_path: str, image_size: int):
        self.labels_path = labels_path
        self.model_path = model_path
        self.image_size = image_size

        with open(self.labels_path, "r") as f:
            self.labels = [line.strip() for line in f]
        
        self.model = tf.keras.models.load_model((self.model_path),
                custom_objects={'KerasLayer':hub.KerasLayer}
                )
    def objetomasgrande(self,V,K):
        A=0
        for i in range(1,K):
            [row,colum]=np.nonzero(V==i)
            Ap=len(row)
            if Ap > A:
                A = Ap 
                row1 = row
                colum1 = colum
        return row1,colum1,A

    def predict_image(self, image: np.ndarray):
        I_HSV =  cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        I_HSV = np.double(I_HSV)
        [M,N,P]=I_HSV.shape 
        H= I_HSV[:,:,0] # COMPONENTE H
        S= I_HSV[:,:,1] # COMPONENTE S
        V= I_HSV[:,:,2] # COMPONENTE V
        umbral1=130
        umbral1_1=180
        [row,colum]=np.nonzero(((H>umbral1 )& (H<umbral1_1)) | ((H>0) & (H<40)))
        Z = np.zeros((M,N))
        for i in range(0,len(colum)):
            Z[row[i],colum[i]]=1
        Z = np.uint8(Z)
        K, V = cv2.connectedComponents(Z, 8) 
        row1,colum1,A = self.objetomasgrande(V,K)
        # print(row1,colum1,A)
        Z1 = np.zeros((M,N))
        for i in range(0,len(colum1)):
            Z1[row1[i],colum1[i]]=1
        kernel = disk(10)
        Z2 = cv2.morphologyEx(Z1, cv2.MORPH_CLOSE, kernel)
        Z2 = cv2.morphologyEx(Z2, cv2.MORPH_OPEN, kernel)
        I4_r = np.multiply(Z2,image[:,:,0])
        I4_g = np.multiply(Z2,image[:,:,1])
        I4_b = np.multiply(Z2,image[:,:,2])
        I4 = cv2.merge([I4_r,I4_g,I4_b])
        [x1,y1]=np.nonzero(Z2==1)
        xmin = min(x1)
        xmax = max(x1)
        ymin = min(y1)
        ymax = max(y1)
        I5 = I4[xmin:xmax, ymin:ymax,:]
        I5 =  np.uint8(I5)
        I6 =  cv2.resize(I5,(224,224), interpolation= cv2.INTER_LINEAR)
        # print(I6.shape)
        img = np.array(I6).astype(float)/255
        img = cv2.resize(img, (224,224))
        pred = self.model.predict(img.reshape(-1, 224, 224, 3))
        top_labels = {}
        top_labels_ids = np.flip(np.argsort(pred, axis=1)[0])
        for label_id in top_labels_ids:
            top_labels[self.labels[label_id]] = pred[0,label_id].item()
        pred_label = self.labels[np.argmax(pred)]
        return {'label': pred_label, 'top': top_labels}

    

    def predict_file(self, file):
        img = np.array(Image.open(file))
        # img = np.array(img).astype(float)/255
        return self.predict_image(img)