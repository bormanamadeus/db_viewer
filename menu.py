#! python

import os

from libdb import *

#TODO check english text into class`s functions
class Menu():

    def __init__(self):
        self.db = None 
        self.menu = {'Start': [self._start, ['Load database', 'End']],
                     'End': [self._end, {}],
                     'Load database': [self._loadDB, ['Print info database', 'End']],
                     'Print info database': [self._printDB, ['Print info database', 'Thank', 'End']],
                     'Thank': [self._helloMessage, ['Load database', 'End']]}

    def mainloop(self):
        ''' mainloop - basic loop menu
        In loop view submenu
        '''
        os.system('clear')
        
        #To point start submenu
        submenu = 'Start' 

        while True:
            (function, options) = self.menu[submenu]
            
            #check exit signal, if false end function menu
            if function():
                break
            
            self.__showmenu(options)
            submenu = self.__choiceSubmenu(options)

            os.system('clear')

    def _start(self):
        ''' Initialization '''
        pass

    def __showmenu(self, options):
        print("# ########## #")
        print("# Main menu: #")
        print("# ########## #")
        for (number, option) in enumerate(options):
            print('%s: %s' % (number + 1, option))
     
    def __choiceSubmenu(self, options):
        number_submenu = (lambda: int(input()))()
        number_submenu = number_submenu - 1

        if number_submenu > len(options):
            print('warning: inputing submenu number bigger having')

        return options[number_submenu]

    def _end(self):
        print('"Good bye!"')
        return True    

    def _loadDB(self):
        os.system('clear')
        if not self.db:
            database_dir = getArg()
            print('"Path to database -> %s"\n' % (database_dir))
            self.db = Database(database_dir)
        else:
            print('"Database already load."\n')

    def _printDB(self):
        self.db.printDatabaseInfo()
        print()

    def _helloMessage(self):
        print('"Thank you a million what use this app!"\n')
