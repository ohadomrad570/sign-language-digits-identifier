import consts
from zipfile import ZipFile
import logger
       
def is_zip_file(file_path):
    file_path_tokens = file_path.split(".")
    file_extention = file_path_tokens[len(file_path_tokens)-1]
    if file_extention == consts.ZIP_EXTENTION:
        return True
    return False

def extract_zip(zip_path, extract_files_path): 
    with ZipFile(zip_path, 'r') as zipObj:
        logger.debug("[INFO] Extracting the images from the zip file...")
        zipObj.extractall(extract_files_path)