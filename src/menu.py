"""
by Ohad Omrad
"""


"""
this is the main python file that manege the program according to the user choicess
"""
import os
import Sort_Data_Set
import Extract_Zip_File
import train_model
import classify
import Cheak_Dir
import PrintsForUser
import random   

def options():
    """
    This function prints for the user his options (UI)
    """
    PrintsForUser.printOptions("******************************************")
    PrintsForUser.printOptions("*          USER INTERFACE                *")
    PrintsForUser.printOptions("*                                        *")
    PrintsForUser.printOptions("*   Enter 1 --> create sorted data set   *")
    PrintsForUser.printOptions("*   Enter 2 --> train the model          *")
    PrintsForUser.printOptions("*   Enter 3 --> predict an image         *")
    PrintsForUser.printOptions("*   Enter 4 --> predict random images    *")
    PrintsForUser.printOptions("*   Enter space bar --> exit             *")
    PrintsForUser.printOptions("*                                        *")
    PrintsForUser.printOptions("******************************************")

def case_One(data_set):
    """
    Get: the path to the unsorted data set
    return: 1 -> if the folder we got was zip folder we return the extract one
                 if it ose an ordniry folder we just return the parameter we got
                 (tool for updating)
            2 -> return the path for the sorted data set
    """
    
    extracted_data = Extract_Zip_File.extract_Zip(data_set) # return the folder path after extract (if it was a zip file at first)    
    sorted_data_path = Cheak_Dir.GetDirectory.get_New_Dir("Please enter the path that you want for your main data set folder (with the folder name)\nPath Must be in English!", True)
    """
    we creating an object from type Create_Data_Set
    that get: the path to the datat and the path that the user chose to sort the images
    """
    data_obj = Sort_Data_Set.CreateDataSet(extracted_data , sorted_data_path)
    data_obj.make_All_Floders()  # this mathod creat the folders tree of drictories
    data_obj.initialization_Data()  #this method initializing the folder by the current images 
    
    return extracted_data, sorted_data_path
    

def case_Two(sorted_data_path):
    """
    Get: the path to the updated sorted data set
    return: the model path and the labels path
           the mpdel path -> contains the trained model
           the labels path - contains the labels for each images (for the predict)

    this function call to the handle_train() fanction that locaited in train_model.py file
    """
    
    model_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output model: ")
    lb_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output label binarizer: ")
    
    while model_path == lb_path:
        PrintsForUser.printError("Error - file will be override")
        lb_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output label binarizer: ")
            
    plot_dir = Cheak_Dir.GetDirectory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ")
    
    while model_path == plot_dir or lb_path == plot_dir:
        PrintsForUser.printError("Error - file will be override")
        plot_dir = Cheak_Dir.GetDirectory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ")

    os.mkdir(plot_dir)
    
    train_obj = train_model.TrainModel(sorted_data_path, model_path,lb_path, plot_dir)
    
    train_obj.handle_train() 
    
    return model_path, lb_path


def case_Three(model_path, labels_path):
    """
    Get: the path to the trained model
         the path to the images labels
    
    this function call to the handle_classify() fanction that locaited in classify.py file
    """
    
    image_path = Cheak_Dir.GetDirectory.is_Exsists("Enter the image path:\nPath Must be in English!", True)
    predict_obj = classify.ImagePredictor(model_path, labels_path)  
    predict_obj.handle_classify(image_path)



def case_Four(model_path, labels_path, data_set, new_images_folder):
    """
    Get: the path to the trained model
         the path to the images labels
         the data set
         a folder with unlearned images
    this function predict 11 random images from each folder
    """
    PrintsForUser.printProcess("[INFO] Learned images...")
    cheakPredict(model_path, labels_path, data_set, 4)
    PrintsForUser.printProcess("[INFO] New images...")
    cheakPredict(model_path, labels_path, new_images_folder, 4)
    

   
def cheakPredict(model_path, labels_path, data_set, num):
    
    list_of_images = os.listdir(data_set)
    pre = classify.ImagePredictor(model_path, labels_path)
    
    for i in range(num):
        image_name = random.choice(list_of_images)
        image_path =  data_set+ r"/" + image_name
        pre.handle_classify(image_path)
        list_of_images.remove(image_name)
        
    
def menu():
    flag = True
    options()
    """
    defult directories
    this directoties change according to the user activity
    """
    #directories_file.create_directories_file()
    
    data_set = r"C:\Users\ilano\OneDrive\Desktop\images"
    sorted_data_path = r"C:\Users\ilano\OneDrive\Desktop\Data"
    model_path = r"C:\Users\ilano\OneDrive\Desktop\model_3_data_10.model"
    labels_path = r"C:\Users\ilano\OneDrive\Desktop\lb_3_data_10.pickle"
    new_images_folder = r"C:\Users\ilano\OneDrive\Desktop\MyHand"
    
    while(flag):
        PrintsForUser.printOptions("--> Your Choice: ")
        choice = input("Enter: ")
        
        if choice == '1':
            """
            if the use enter 1 -> the directory of the data will be updated
            """
            data_set, sorted_data_path = case_One(data_set)
            PrintsForUser.printProcess("[INFO] Using new data set")
    
        if choice == '2':
            """
            if the use enter 2 -> the directory of the model and the labeld will be updated
            """
            model_path,labels_path =  case_Two(sorted_data_path)
            PrintsForUser.printProcess("[INFO] Using trained model")
         
        if choice == '3':
            """
            if the use enter 3 -> the program will use the updated directory and predict the image
            """
            case_Three(model_path,labels_path)
            
        if choice == '4':
            case_Four(model_path,labels_path, data_set, new_images_folder)
            
        if choice == ' ':
            PrintsForUser.printProcess("[INFO] Exiting...")
            flag = False
    
    
if __name__ == "__main__":
    menu()