"""
by Ohad Omrad
"""


"Extract zip file"

from zipfile import ZipFile
import Cheak_Dir
import PrintsForUser

def extract_Zip_app(path):
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(path, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        if zipObj.is_zipfile(path):
            ls = path.split(".")
            path = ""
            for i in range(len(ls) - 1):
                path += ls[i]
                            
            zipObj.extractall(path)
    return path
            
    
def extract_Zip(zip_path): 
    
    path = zip_path
    """
    ls is a list of put substring thar split by '.'
    """
    ls = zip_path.split(".")
    """
    we cheak if the file/folder is zip by its ending - file type
    """
    if ls[len(ls)-1] == "zip":
        PrintsForUser.printProcess("[INFO] Got a zip file...")
        path = Cheak_Dir.GetDirectory.get_New_Dir("Choose the path to extract the files (with a new folder name)")   
        """
        extract the folder to new location that the user chose
        """        
        with ZipFile(zip_path, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            PrintsForUser.printProcess("[INFO] Extracting the images from the zip file...")
            zipObj.extractall(path)
        
        PrintsForUser.printProcess("[INFO] Finished extracting process...")

    else:
        PrintsForUser.printProcess("[INFO] Got ordinary file...")
    return path
            
            
            
   