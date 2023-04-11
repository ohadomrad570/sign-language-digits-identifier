import os
import string
import errors

class DirectoryHander():
    @staticmethod
    def is_path_name_contains_hebrew(path):
        for ch in path:
            if not (ch in string.printable):
                True
        return False
    
    @staticmethod
    def is_exists(path):
        if not os.path.exists(path):
            return False
        return True
    
    @staticmethod
    def create_directory(path):
        if(DirectoryHander.is_exists(path)):
            raise errors.PathAlreadyExists()
        try:
            os.mkdir(path)
            return True
        except:
            raise errors.PathNotValid('Creation of the directory %s failed: ' + path)
            