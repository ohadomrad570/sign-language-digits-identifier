import os
import utils
import services
import random   
import logger
import handlers

def create_sorted_data_set(data_set, sorted_data_path):
    extracted_data = utils.extract_zip(data_set) 
    data_obj = services.CreateDataSet(extracted_data , sorted_data_path)
    data_obj.create_all_folders()  
    data_obj.initialization_data()
    return extracted_data, sorted_data_path
    

def train_the_model(sorted_data_path, model_path, lb_path, plot_dir):
    handlers.DirectoryHander.create_directory(plot_dir)
    train_obj = services.TrainModel(sorted_data_path, model_path,lb_path, plot_dir)
    train_obj.handle_train() 
    return model_path, lb_path


def predict_image(model_path, labels_path, image_path): 
    predict_obj = services.ImagePredictor(model_path, labels_path)  
    predict_obj.handle_classify(image_path)



def predict_random_images(model_path, labels_path, data_set, new_images_folder):
    logger.info("[INFO] Learned images...")
    predict_random_images(model_path, labels_path, data_set, 4)
    logger.info("[INFO] New images...")
    predict_random_images(model_path, labels_path, new_images_folder, 4)
   
   
def predict_random_images(model_path, labels_path, data_set, num):
    
    list_of_images = os.listdir(data_set)
    pre = services.ImagePredictor(model_path, labels_path)
    
    for i in range(num):
        image_name = random.choice(list_of_images)
        image_path =  data_set+ r"/" + image_name
        pre.handle_classify(image_path)
        list_of_images.remove(image_name)
        