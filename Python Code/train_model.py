"""
by Ohad Omrad
"""

"""
this python file handle the train section
"""


import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split



import Model

import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import random
import pickle
import cv2
import os

import PrintsForUser


class TrainModel():
    
    def __init__(self, dataset_path, model_path, labels_path, plot_dir):
        
        self.__dataset_path = dataset_path # the data set directory
        self.__model_path = model_path    # the directory the user chose to save the trained model
        self.__labels_path = labels_path #the directory the user chose to save the images labels
        self.__plot_dir = plot_dir        # the directory to the folder that the user chose to save the graph images
        
        self.__EPOCHS = 10  #number of epochs
        self.__INIT_LR = 1e-3  #learning rate
        self.__BS = 32 #batch size
        self.__IMAGE_DIMS = (50, 50, 1) #image dimensions
        self.__data = []   # list of all the images as arrays
        self.__labels = []  #list labels of all the images
        
        

    def handle_train(self):
    
        """
        this public method manage the train section
        return the train model path and the images labels path
        """
        
        self.__loading_Images()
        self.__scale_Pixels()
    
        history = self.__train()
    
        self.__graph1(history, self.__plot_dir+ r"\plot1.png")
        self.__graph2(history, self.__plot_dir +r"\plot2.png")
    
    
    
    def __loading_Images(self):
        """
        this method load the images from the current directory
        """
        # grab the image paths and randomly shuffle them
        PrintsForUser.printProcess("[INFO] Loading images...")
        imagePaths = sorted(list(paths.list_images(self.__dataset_path)))
        random.seed(42)
        random.shuffle(imagePaths)

        # loop over the data set images
        for imagePath in imagePaths:
            """ 
                load the image as gray scale, convert it to numpy array and store it in the data list
            """
            image = cv2.imread(imagePath)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (self.__IMAGE_DIMS[1], self.__IMAGE_DIMS[0]))
            image = img_to_array(image)
            self.__data.append(image)
            
            """
            extract the class label from the image path and update the labels list
            """
            label = imagePath.split(os.path.sep)[-2]
            self.__labels.append(label)
        
 
    def __scale_Pixels(self):    
        """ 
        this method scale the images pixels to range [0, 1] from range [0, 255]
        the data list store all the images by arrays
        so by convert this list we convert all the images pixels range
        
        return:  the labels binary file
        """
        self.__data = np.array(self.__data, dtype="float") / 255.0
        self.__labels = np.array(self.__labels)
        PrintsForUser.printProcess("[INFO] data matrix: {:.2f}MB".format(self.__data.nbytes / (1024 * 1000.0)))
    
    
    
    def __train(self):
    
        #binarize the labels (this is an easy tool for classification

        lb = LabelBinarizer()
    
        #Linear transformation
        self.__labels = lb.fit_transform(self.__labels)

        """
        partition the data into training and testing splits using 80% of
        the data for training and the remaining 20% for testing
        """
        
        (trainX, testX, trainY, testY) = train_test_split(self.__data,
        	self.__labels, test_size=0.2, random_state=42)
     
        
        
        # construct the image generator for data augmentation
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	        horizontal_flip=True, fill_mode="nearest")

        
        # initialize the model
        PrintsForUser.printProcess("[INFO] Compiling model...")
        model = Model.MyModel.build(width=self.__IMAGE_DIMS[1], height=self.__IMAGE_DIMS[0],
	    depth= self.__IMAGE_DIMS[2], classes=len(lb.classes_))
        
        opt = Adam(lr=self.__INIT_LR, decay=self.__INIT_LR / self.__EPOCHS)
        
        model.compile(loss="categorical_crossentropy", optimizer=opt,
	        metrics=["accuracy"])
        
        model.summary()
        # train the network
        PrintsForUser.printProcess("[INFO] Training network...")
        
        H = model.fit_generator(
	    aug.flow(trainX, trainY, batch_size=self.__BS),
	    validation_data=(testX, testY),
	    steps_per_epoch=len(trainX) // self.__BS,
	    epochs=self.__EPOCHS, verbose=1)
        

        # Evaluate the model on the test data using `evaluate`
        PrintsForUser.printProcess('\n# Evaluate on test data')
        results = model.evaluate(testX, testY, batch_size=32)
        PrintsForUser.printProcess('test loss, test acc:' + results)
        
        
        # save the model to disk
        PrintsForUser.printProcess("[INFO] Serializing network...")
        model.save(self.__model_path)
    
        # save the label binarizer to disk
        PrintsForUser.printProcess("[INFO] Serializing label binarizer...")
        f = open(self.__labels_path, "wb")
        f.write(pickle.dumps(lb))
        f.close()
        return H


    def __graph2(self, history, plot_path):
        
        """
        Gat: the history and the path that the user chose to save the results
        create an images that contains the graph
        """
	    # plot loss
    
        plt.subplot(211)
        plt.title('Cross Entropy Loss')
        plt.plot(history.history['loss'], color='blue', label='train')
        plt.plot(history.history['val_loss'], color='orange', label='test')
	    # plot accuracy
        plt.subplot(212)
        plt.title('Classification Accuracy')
        plt.plot(history.history['accuracy'], color='blue', label='train')
        plt.plot(history.history['val_accuracy'], color='orange', label='test')
	    # save plot to file
        plt.savefig(plot_path)
        plt.close()
    
    
    
    def __graph1(self,H, plot_path):
        """
        Gat: the history and the path that the user chose to save the results
        create an images that contains the graph
        """
        # plot the training loss and accuracy
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


   

"""
def handle_app(dataset_path,model_path,lb_path, plot_path ):
    loading_Images(dataset_path)
    data_sacaild, labels_np, lb = scale_Pixels()
    
    history = train(data_sacaild, labels_np, lb, model_path, lb_path)
    
    graph1(history, plot_path)
    
    return model_path, lb_path
    
"""

    
    
    


    

