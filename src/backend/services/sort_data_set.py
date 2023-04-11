import shutil
import os
import random
from abc import ABC, abstractmethod
import logger
import handlers

class DataSet(ABC):
    
    @abstractmethod
    def __init__(self, data_set , main_folder):
        self._data_set_dir = data_set
        self._main_folder_path = main_folder
       
    @abstractmethod
    def create_all_folders(self):
        pass
    
    @abstractmethod
    def initialization_data(self):
        pass


       
class SignLanguageDataSet(DataSet):
    def __init__(self,data_set , main_folder):
        super(SignLanguageDataSet, self).__init__(data_set , main_folder)
        self._directories = [] 
        self._num_categories = 10
        
    def _num_switcher(self, s):
        dic={"num0":0, "num1":1, "num2":2, "num3":3,"num4":4, "num5":5, 
                  "num6":6, "num7":7 , "num8":8, "num9":9}
        return dic.get(s)


    def _get_image_category(self, image_name):
        image_splite_name = image_name.split('_')
        sign_num = image_splite_name[0]
        return self._num_switcher(sign_num)

    @abstractmethod
    def _get_image_category(self):
        pass
    
    
    @abstractmethod
    def initialization_data(self):
        pass
    

class CreateDataSet(SignLanguageDataSet):
    
    def __init__(self,data_set , main_folder):
        super(CreateDataSet, self).__init__(data_set , main_folder)
        
    def _get_image_category(self):
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
        
        logger.debug("[INFO] Creating folders...")
        handlers.DirectoryHander.create_directory(self._main_folder_path)
        for i in range(self._num_categories):
            path = self._main_folder_path + r"\num_" + str(i)
            self._directories.append(path)
            handlers.DirectoryHander.create_directory(path)
    
    
    def initialization_data(self):
        logger.debug("[INFO] Initializing the folders...")
        list_of_images = os.listdir(self._data_set_dir)
        
        while(len(list_of_images)>=1):
            image_name = random.choice(list_of_images)
            num = self._get_image_category(image_name)
            shutil.copy(self._data_set_dir + r"/" + image_name,self._directories[num])
            list_of_images.remove(image_name)
          

            