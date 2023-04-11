import PrintsForUser
import backend
import env
from handlers import InputHandler
import consts


def create_sorted_data_set_proxy():
    sorted_data_path = InputHandler.get_directory(consts.GET_DIRECTORY_MESSAGE)
    env.extracted_data, env.sorted_data_path = backend.create_sorted_data_set(env.data_set, sorted_data_path)
    PrintsForUser.printProcess("[INFO] Using new data set")
    return True

def train_the_model_proxy():

    model_path = InputHandler.get_directory(consts.GET_MODEL_MESSAGE)
    lb_path = InputHandler.get_directory(consts.GET_LABELS_MESSAGE)
    
    while model_path == lb_path:
        PrintsForUser.printError("Error - file will be override")
        lb_path = InputHandler.get_directory(consts.GET_LABELS_MESSAGE)
            
    plot_dir = InputHandler.get_directory(consts.GET_PLOT_MESSAGE)
    
    while model_path == plot_dir or lb_path == plot_dir:
        PrintsForUser.printError("Error - file will be override")
        plot_dir = InputHandler.get_directory(consts.GET_PLOT_MESSAGE)
    
    env.model_path, env.lb_path = backend.train_the_model(env.sorted_data_path, model_path,lb_path, plot_dir)
    PrintsForUser.printProcess("[INFO] Using trained model")
    return True

def predict_image_proxy():
    image_path =  InputHandler.get_directory(consts.GET_IMAGE_MESSAGE)
    backend.predict_image(env.model_path, env.labels_path, image_path)
    return True


def predict_random_images_proxy():
   backend.predict_random_images(env.model_path, env.labels_path, env.data_set, env.new_images_folder)
   return True


def exit():
    PrintsForUser.printProcess("[INFO] Exiting...")
    return False
