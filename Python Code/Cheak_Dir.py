"""
by Ohad Omrad
"""

"""
this python file handle the input section
"""

import os
import PrintsForUser
import string

class GetDirectory():
    
    @staticmethod
    def is_Exsists(massage, flagLang = False):
        """
        Get: 1 -> A message to desplay for the user
             2 -> launguge flag - if true -> hebrew letters will consider as an error
          
            this function requset an exsisting directory from the user and return it only if cheak_exsists_dir() function return true
            this function keep requset a directory until it be valid according to the cheak function
            """
        PrintsForUser.printOptions(massage)
        path = input("Enter: ")

        while not GetDirectory.__cheak_Exsists_Dir(path, flagLang):
            PrintsForUser.printOptions(massage)
            path = input("Enter: ")
            
        return path
    
    @staticmethod
    def __cheak_Launguge(path):
        """
        Get: path
        if the path in not allowed to contain hebrew letters
        this function cheak if the path contain only English letters
        """
        for ch in path:
            if not (ch in string.printable):
                PrintsForUser.printError("Error - path contains hebrew letters")
                return False
        
        return True
    
    @staticmethod
    def __cheak_Exsists_Dir(path, flagLang):
        """
        Get: path, launguge flag -> if true -> hebrew letters will consider as an error
        this requset an exsists directory from the user and return it only the current directory exsists
        return true only if the path is valid  
        """
    
        if(flagLang):
            if(not GetDirectory.__cheak_Launguge(path)):
                return False
        
        if not os.path.exists(path):
            PrintsForUser.printError("Error - no such file or directory")
            return False
    
        return True
    
    @staticmethod
    def get_New_Dir(massage,flagLang = False):
        """
        Get: 1 -> A message to desplay for the user
             2 -> launguge flag - if its true - > hebrew letters will consider as an error
                  the difault is false
    
        this function requset a new directory from the user and return it only if cheak_new_dir() function return true
        this function keep requset a directory until it be valid according to the cheak function
        """
    
        path = ""
    
        while not GetDirectory.__cheak_New_Dir(path, flagLang):
            PrintsForUser.printOptions(massage)
            path = input("Enter: ")
        return path 
   
    
    @staticmethod
    def __cheak_New_Dir(path, flagLang):
        """
        Get: a path, a language flag
        return true if the path is vaild and new one else return false
        """

        if(flagLang):
            if(not GetDirectory.__cheak_Launguge(path)):
                return False
       
        if(os.path.exists(path)):
            """
            cheak that the path is not allready exisist
            if it allrrady exisists return false
            """
            PrintsForUser.printError("Error - this directory is allready exsists")
            return False
    
        try:
            """
            try to make a folder in the current path
            if its succed the path is valid
            else
            the path is not vaild and the function return false
            """
            os.mkdir(path)
            os.rmdir(path)
            return True
         
        except:
            if(path != ""):
                PrintsForUser.printError("Error - directory is not valid")            
                return False
            