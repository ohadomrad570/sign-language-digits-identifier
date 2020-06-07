"""
by Ohad Omrad
"""


import shutil
import os
import random
from abc import ABC, abstractmethod
import PrintsForUser

"""
path to all images: C:\\Users\\ilano\\OneDrive\\Desktop\\images
data_set = r"C:\\Users\\ilano\\OneDrive\\Desktop\\images"
"""

"""
an abstruct class that declares the structer of Data_Set and the methods that any subclass of it need to realize
"""

class DataSet(ABC):
    
    @abstractmethod
    def __init__(self, data_set , main_folder):
        """
        Data_Set Constactor:
        Get: data_set  =  path to the all images
             main_folder  =  path to the folder which the user chose to sort the images
        """
        self._data_set_dir = data_set
        self._main_folder_path = main_folder
         
    def _make_Folder(self, path):
        """
        input: the current puth to create a folder
        output: a folder created
        """
    
        try:
            os.mkdir(path)

        except:
            PrintsForUser.printError("Error - Creation of the directory %s failed: " + path)
            
    @abstractmethod
    def make_All_Folders(self):
        pass
    
    @abstractmethod
    def initialization_Data(self):
        pass

"""
an abstruct class that inheritance from "Data_Set" class and declares the structer of general Sign Language Data Set
"""
       
class SignLanguageDataSet(DataSet):
    def __init__(self,data_set , main_folder):
        """
        Sign_Language_Data_Set Constactor:
        Get: data_set  =  path to the all images
             main_folder  =  path to the folder which the user chose to sort the images
        """
        super(SignLanguageDataSet, self).__init__(data_set , main_folder)
        self._directories = []  # a list of all the direction that we will create in our "make_All_Floders" method
        self._num_categories = 10 #the num of folders
        
    def _num_Switcher(self, s):
        """
        input: get a key
        output: return the value of the key
        this method converten the name to the number it describe
        """
        dic={"num0":0, "num1":1, "num2":2, "num3":3,"num4":4, "num5":5, 
                  "num6":6, "num7":7 , "num8":8, "num9":9}
        return dic.get(s)


    def _get_Image_Category(self, image_name):
        """
        input: image name
        output: return the sign launguge number that the image represent the number of hand
        """
        image_splite_name = image_name.split('_')
        sign_num = image_splite_name[0]
        return self._num_Switcher(sign_num)


    
    @abstractmethod
    def make_All_Folders(self):
        pass
    
    
    @abstractmethod
    def initialization_Data(self):
        pass
    

"""
a class that inheritance from "Sign_Language_Data_Set" class and realize all the abstrucat methods
this class is responsible to create an sorted data set according to its class categories 
"""
class CreateDataSet(SignLanguageDataSet):
    
    def __init__(self,data_set , main_folder):
        """
        Create_Data_Set Constactor:
        Get: data_set  =  path to the all images
             main_folder  =  path to the folder which the user chose to sort the images
        """
        super(CreateDataSet, self).__init__(data_set , main_folder)
        
    def make_All_Folders(self):
        """
        -- mainFolder:
            -- num0
            -- num1
            -- num2
            -- num3
            -- num4
            -- num5
            -- num6
            -- num7
            -- num8
            -- num9
            -- num10
        """
        
        PrintsForUser.printProcess("[INFO] Creating folders...")
        self._make_Folder(self._main_folder_path)
        for i in range(self._num_categories):
            path = self._main_folder_path + r"\num_" + str(i)
            self._directories.append(path)
            self._make_Folder(path)
    
    
    def initialization_Data(self):
        """
        in each folder putt the relevent images in the relevent folder
        its initialization the data according to its class categorical 
        """
        PrintsForUser.printProcess("[INFO] Initializing the folders...")
        list_of_images = os.listdir(self._data_set_dir)
        
        while(len(list_of_images)>=1):
            image_name = random.choice(list_of_images)
            num = self._get_Image_Category(image_name)
            shutil.copy(self._data_set_dir + r"/" + image_name,self._directories[num])
            list_of_images.remove(image_name)
          

            