import PrintsForUser
import consts
from options import optionsMapper

def menu():
    flag = True
    PrintsForUser.printOptions(consts.MENU)
    while(flag):
        PrintsForUser.printOptions("--> Your Choice: ")
        choice = input("Enter: ")
        chosenFunction = optionsMapper.get(choice)
        flag = chosenFunction()
    
if __name__ == "__main__":
    menu()