"""
by Ohad Omrad
"""

"""
    this file contains the function that prints messages for the user in colors
"""


from colorama import init, Fore, Back, Style
    
def printError(message):
    """
    Get: message
    prints it in red
    """
    init(convert=True)
    print(Fore.RED + message) 
    Style.RESET_ALL
    
def printOptions(message):
    """
    Get: message
    prints it in green
    """
    init(convert=True)
    print(Fore.GREEN + message) 
    Style.RESET_ALL
        
def printProcess(message):
    """
    Get: message
    prints it in blue
    """
    init(convert=True)
    print(Fore.BLUE + message) 
    Style.RESET_ALL
    
    
    
    
    