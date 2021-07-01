#! python # -*- coding: 

import sys
import os
from pypxlib import Table

def getArg():
    ''' 
        Get name database from command line arguments
    '''
    arg_cmd = []

    for param in sys.argv:
        arg_cmd.append(param)

    if len(arg_cmd) <= 1:
        print('--> Error: At least one parametr must be present!\n-->        "db_viewer.py <path name to database>"')
        exit()

    #return dir to database
    return arg_cmd[1]

ENTRY_TYPE = {}

OPERATOR_TYPE = {')=': 1,
                 '(': 14,
                 'или': 10}

MAX_LINE = 50

NAME_DATABASE_FILE = 'Pnl_info.db'
NAME_LOGIC_FILE = 'pnl_logc.db'
NAME_INPUTS_FILE = 'pnl_inpt.db'
NAME_OUTPUTS_FILE = 'pnl_oupt.db'

ELEMENT_NUMBER_COLUMN = 'Par.0'
ELEMENT_TYPE_COLUMN = 'Opnd Num'
OPERATOR_TYPE_COLUMN = 'Optr Num'


class Element():

    def __init__(self,
                 number,
                 etype,
                 description,
                 panel,
                 level=0):

        self.__number = number
        self.__etype = etype
        self.__description = description 
        self.__panel = panel
        self.__level = level
        self.__tab = '\t' * self.__level

        self.__children = {}

    def getNumber(self):
        return self.__number

    def getType(self):
        return self.__etype

    def getDescription(self):
        return self.__description

    def getPanel(self):
        return self.__panel

    def getLevel(self):
        return self.__level

    def getTab(self):
        return self.__tab

    def getChildren(self):
        return self.__children

    def findChildren(self):
        table_operator = {')=': 1}
        status_find_child = False
        path_logic_file = self.__panel.getFolder() + '\\' + NAME_LOGIC_FILE

        with Table(path_logic_file) as inputs:

            for row in inputs: 
                if row['Operator'].encode('cp850').decode('cp1251') == 'конец':
                    break

                #if str(row['Par.0']) == str(self.__number) and\
                if str(row[ELEMENT_NUMBER_COLUMN]) == str(self.__number) and\
                   str(row[ELEMENT_TYPE_COLUMN]) !=  table_operator[')='] and\
                   str(row[ELEMENT_TYPE_COLUMN]) !=  table_operator[')='] and\
                   status_find_child == False:
                       #print('Find matching, string number: ', str(row['Line']))
                       #print('Number element: ', str(row['Par.0']), 'Type: ', 'Optr Num: ', 'Operation type: ', str(row['Opnd Num']), 'Type element: ', str(self.__etype))
                       status_find_child = True

                if status_find_child == True and\
                   row[OPERATOR_TYPE_COLUMN] == table_operator[')=']:
                    print('Find child line: ', str(row['Line']), 
                          'Number: ', str(row['Par.0']),
                          'Type: ', str(row['Opnd Num']))
                    self.createChild(row[ELEMENT_NUMBER_COLUMN], row[ELEMENT_TYPE_COLUMN])

                    status_find_child = False

    def createChild(self, numberchild, typechild):
        print(numberchild, typechild)
        self.__children[(numberchild, typechild)] = ENTRY_TYPE[typechild]\
                                                              (numberchild,
                                                               '',
                                                               '',
                                                               self.__panel,
                                                               ++self.__level)
        #with Table(self.__panel + '\\' + NAME_INPUTS_FILE) as inputs:
        #    row = inputs[numberchild]
        #    self.__children[numberchild] = (typechild, \
        #        Input(self.__panel, '', numberchild, typechild, \
        #            row['Input text'], '\t'))

    def findChildrenOfChildren(self):
        print('findChildrenOfChildren') 
        for typechild, input in self.__children.values():
            print('typechild: ', typechild)
            #if typechild in [ENTRY_TYPE['input'], \
            if typechild in [ENTRY_TYPE['marker'], \
                             ENTRY_TYPE['timer']]:
                print('*Find typechild*')
                input.findChildren()
                input.printChildren()


class Input(Element):
    """
        Class Input - class contains information about the input of the fire panel
    """
    pass
    #entrytype = ENTRY_TYPE['Input']


class Exit(Element):
    pass
    #entrytype = ENTRY_TYPE['exit']


class Marker(Element):
    pass
    #entrytype = ENTRY_TYPE['marker']


class Timer(Element):
    pass
    #entrytype = ENTRY_TYPE['timer']


ENTRY_TYPE = {1: Input,
              2: Exit, 
              3: Marker,
              4: Timer}


class Panel():
    # Class of database station
    def __init__(self, panel_folder):
        self.__panel_folder = panel_folder
        self.__path_logic_file = self.__panel_folder + '\\' + NAME_LOGIC_FILE
        self.__rows = []
        self.__inputs = {} 
        self.__outputs = {} 

        self.__getPanelProgram()
        self.__getInputsInfo()
        self.__getOutputsInfo()
        
    def __getPanelProgram(self):
        with Table(self.__path_logic_file) as logic_file:
            for row in logic_file:
                self.__rows.append(row)

    def __getInputsInfo(self):
        with Table(self.__panel_folder + '\\' + NAME_INPUTS_FILE) as inputs:
            for row in inputs:
                number = str(row['Input']).encode('cp850')\
                                          .decode('cp1251')
                itype = str(row['Type']).encode('cp850')\
                                        .decode('cp1251')
                description = str(row['Input text']).encode('cp850')\
                                                    .decode('cp1251')

                if itype in ['Нет', 'None']:
                    continue
                
                self.__inputs[number] = Input(number,
                                              itype,
                                              description,
                                              self)

    def __getOutputsInfo(self):
        with Table(self.__panel_folder + '\\' + NAME_OUTPUTS_FILE) as outputs:
            for row in outputs:
                number = str(row['Output']).encode('cp850')\
                                          .decode('cp1251')
                otype = str(row['Type']).encode('cp850')\
                                        .decode('cp1251')
                description = str(row['Output text']).encode('cp850')\
                                                     .decode('cp1251')

                if otype in ['Нет', 'None']:
                    continue
                
                self.__outputs[number] = Input(number,
                                               otype,
                                               description,
                                               self)

    def getFolder(self):
        return self.__panel_folder

    def getLogicFile(self):
        return self.__path_logic_file

    def getInputs(self):
        return self.__inputs

    def getOutputs(self):
        return self.__outputs

    
class Database():
    def __init__(self, dir_path):
        """
            Input arguments:
            path - database path

            Open functions:
            getPanels() - return a list of panels
        """
        self.__dir_path = dir_path
        func = (lambda s=self.__dir_path: '' if s[-1] == '\\' else '\\')
        self.__file_path = self.__dir_path + func() + NAME_DATABASE_FILE

        self.__work_dir = None
        self.__panels_path = {}
        self.__panels_db = {}

        self.__getPathOfPanels() # set self.__panels_path
        self.__getPanelsDatabase() # set self.__panels_db

    def __getPathOfPanels(self):
        """
            Get the path of the panels
        """
            
        with Table(self.__file_path) as db:
            self.__work_dir = os.path.dirname(self.__file_path)
            
            for panel in db:
                if panel['Panel Name'] is not None:
                    panel_dir = self.__work_dir + '\\' + panel['Panel Name']
                    if os.path.exists(panel_dir):
                        self.__panels_path[panel['Panel Name']] = panel_dir

    def __getPanelsDatabase(self):
        """
            Get database of panels 
        """

        for (panel_name, panel_path) in self.__panels_path.items():
            self.__panels_db[panel_name] = Panel(panel_path) 

    def printDatabaseInfo(self):
        """ 
            To Print the database information
        """ 
        print('"To Print the database information"\n')
        print('1. Database directory: %s' % (self.__work_dir))
        print('2. List of panels:')

        for panel_name, panel_path in self.__panels_path.items():
            print("\t%s -> %s" % (panel_name, panel_path))

    def getPanels(self):
        return self.__panels_db 


if __name__ == '__main__':
    pass
