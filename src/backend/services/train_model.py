import matplotlib
matplotlib.use("Agg")


from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from tensorflow.keras.utils import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

from model import MyModel

import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import random
import pickle
import cv2
import os
import logger


class TrainModel():
    
    def __init__(self, dataset_path, model_path, labels_path, plot_dir):
        
        self.__dataset_path = dataset_path 
        self.__model_path = model_path    
        self.__labels_path = labels_path 
        self.__plot_dir = plot_dir     
        
        self.__EPOCHS = 10  
        self.__INIT_LR = 1e-3
        self.__BS = 32 
        self.__IMAGE_DIMS = (50, 50, 1)
        self.__data = []   
        self.__labels = []
        
        

    def handle_train(self):
        self.__loading_images()
        self.__scale_pixels()
    
        history = self.__train()
    
        self.__graph1(history, self.__plot_dir+ r"\plot1.png")
        self.__graph2(history, self.__plot_dir +r"\plot2.png")
    
    
    
    def __loading_images(self):

        # grab the image paths and randomly shuffle them
        logger.info("[INFO] Loading images...")
        imagePaths = sorted(list(paths.list_images(self.__dataset_path)))
        random.seed(42)
        random.shuffle(imagePaths)

        # loop over the data set images
        for imagePath in imagePaths:
            image = cv2.imread(imagePath)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (self.__IMAGE_DIMS[1], self.__IMAGE_DIMS[0]))
            image = img_to_array(image)
            self.__data.append(image)

            label = imagePath.split(os.path.sep)[-2]
            self.__labels.append(label)
        
 
    def __scale_pixels(self):    
        self.__data = np.array(self.__data, dtype="float") / 255.0
        self.__labels = np.array(self.__labels)
        logger.info("[INFO] data matrix: {:.2f}MB".format(self.__data.nbytes / (1024 * 1000.0)))
    
    
    
    def __train(self):
    
        lb = LabelBinarizer()
        self.__labels = lb.fit_transform(self.__labels)
        (trainX, testX, trainY, testY) = train_test_split(self.__data,
        	self.__labels, test_size=0.2, random_state=42)
    
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	        horizontal_flip=True, fill_mode="nearest")

        
        logger.info("[INFO] Compiling model...")
        model = MyModel.build(width=self.__IMAGE_DIMS[1], height=self.__IMAGE_DIMS[0],
	    depth= self.__IMAGE_DIMS[2], classes=len(lb.classes_))
        
        opt = Adam(lr=self.__INIT_LR, decay=self.__INIT_LR / self.__EPOCHS)
        
        model.compile(loss="categorical_crossentropy", optimizer=opt,
	        metrics=["accuracy"])
        
        model.summary()
        logger.info("[INFO] Training network...")
        
        H = model.fit_generator(
	    aug.flow(trainX, trainY, batch_size=self.__BS),
	    validation_data=(testX, testY),
	    steps_per_epoch=len(trainX) // self.__BS,
	    epochs=self.__EPOCHS, verbose=1)
        

        logger.debug('\n# Evaluate on test data')
        results = model.evaluate(testX, testY, batch_size=32)
        print('test loss ' + str(results[0])  + ' , test acc ' + str(results[1]))        
        
        
        logger.info("[INFO] Serializing network...")
        model.save(self.__model_path)
    
        logger.info("[INFO] Serializing label binarizer...")
        f = open(self.__labels_path, "wb")
        f.write(pickle.dumps(lb))
        f.close()
        return H


    def __graph2(self, history, plot_path):
        plt.subplot(211)
        plt.title('Cross Entropy Loss')
        plt.plot(history.history['loss'], color='blue', label='train')
        plt.plot(history.history['val_loss'], color='orange', label='test')
        plt.subplot(212)
        plt.title('Classification Accuracy')
        plt.plot(history.history['accuracy'], color='blue', label='train')
        plt.plot(history.history['val_accuracy'], color='orange', label='test')
        plt.savefig(plot_path)
        plt.close()
    
    
    
    def __graph1(self,H, plot_path):
        plt.style.use("ggplot")
        plt.figure()
        N = self.__EPOCHS
        plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
        plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig(plot_path)
