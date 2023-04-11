from colorama import init, Fore, Back, Style
    
def printError(message):
    init(convert=True)
    print(Fore.RED + message) 
    Style.RESET_ALL
    
def printOptions(message):
    init(convert=True)
    print(Fore.GREEN + message) 
    Style.RESET_ALL
        
def printProcess(message):
    init(convert=True)
    print(Fore.BLUE + message) 
    Style.RESET_ALL
    