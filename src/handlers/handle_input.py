# import backend
import PrintsForUser

class InputHandler():
    def get_directory(massage):
        path = ""
        valid_directory = False
        while not valid_directory:
          try:
              PrintsForUser.printOptions(massage)
              path = input("Enter: ")
              if not backend.DirectoryHander.is_path_name_contains_hebrew(path):
                backend.DirectoryHander.create_directory(path)
                valid_directory = True
          except Exception as e:
              PrintsForUser.printError(e)