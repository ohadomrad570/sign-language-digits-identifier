from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import pickle
import cv2
import os
import logger

IMAGE_SIZE = (50,50)

class ImagePredictor():
    
    def __init__(self, model_path, labels_path):
        self.__model_path = model_path
        self.__labels_path = labels_path
        self.__image_path = ""
        self.__model = None
        self.__lb = None
        
    def handle_classify(self,image_path):
    
        """
        Get: the trained model path and the images labels path
        this finction manege the classify
        """
        
        self.__load_Model()
        self.__image_path = image_path
        image_arr, output = self.__load_Image()
        self.__predict_Image(image_arr, output)


    def __load_Model(self):
        """
        load the trained convolutional neural network and the label binarizer
        """
        logger.info("[INFO] Loading network...")
        
        self.__model = load_model(self.__model_path)
        self.__lb = pickle.loads(open(self.__labels_path, "rb").read())
    
    
    def __load_Image(self):
        """
        Get: an image path
        this finction load the image that the user pass as its path as a parameter
        return: 1 -> the image numpy array (after fitting the image colors, dims, pixels scale... )
               2->copy of the image as gray scale
        """
        # load the image
        image = cv2.imread(self.__image_path)
        output = image.copy()
        # pre-process the image for classification

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, IMAGE_SIZE)
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return image, output


    def __predict_Image(self,image_arr, output):
        """
        Get:  1 -> the image as array      
              2 -> copy of the image
        """
        # classify the input image
        logger.info("[INFO] Classifying image...")
        proba = self.__model.predict(image_arr)[0]
        idx = np.argmax(proba)
        label = self.__lb.classes_[idx]

        """
        we will prints "correct" if the input image label is fit to the prediction label
        else we will print "incorrect"
        """
    
        filename = self.__image_path[self.__image_path.rfind(os.path.sep) + 1:]
        correct = "correct" if filename.rfind(label) != -1 else "incorrect"
        
        """
        bulid the label and draw the label ont he image
        """
        label = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
        output = imutils.resize(output, width=400)
        cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,	0.7, (0, 255, 0), 2)
        
        # show the output image
        logger.info("[INFO] {}".format(label))
        cv2.imshow("Output", output)
        cv2.waitKey(0)    

"""
def handle_app(model_path, labels_path,image_path ):
    model, lb = load_Model(model_path , labels_path)
    image_arr, output = load_Image(image_path)
    predict_Image(model, lb, image_arr, image_path, output)
    
"""

    
    
    