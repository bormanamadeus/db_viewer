#! python

import os

from libdb import *


menu = {}
db = None 

def mainloop():
    '''
    '''
    os.system('clear')
    
    #To point start submenu
    submenu = 'Start' 
    final = False

    while not final:
        (function, options) = menu[submenu]
        
        #check exit signal
        if function():
            break
        
        showmenu(options)
        submenu = choiceSubmenu(options)

        os.system('clear')

def start():
    print('start job')

def showmenu(options):

    for (number, option) in enumerate(options):
        print('%s: %s' % (number + 1, option))
 
def choiceSubmenu(options):
    number_submenu = (lambda: int(input()))()
    number_submenu = number_submenu - 1

    if number_submenu > len(options):
        print('warning: inputing submenu number bigger having')

    return options[number_submenu]

def end():
    print('end job')
    return True    

def loadDB():
    global db

    print('loadDB job')
    name_fire_panel = getArg()
    print(name_fire_panel)
    db = Database(name_fire_panel)
    print(db)

def printDB():
    global db

    print('printDB job')
    #put dir to database
    print(db)
    db.printDatabaseInfo()

def helloMessage():
    print('Thank you a million what use this app!')

menu = {'Start': [start, ['Load database', 'End']],
        'End': [end, {}],
        'Load database': [loadDB, ['Print info database', 'End']],
        'Print info database': [printDB, ['Print info database', 'Thank', 'End']],
        'Thank': [helloMessage, ['Print info database', 'End']]}

