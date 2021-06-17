#! python # -*- coding: 

import sys
import os
from pypxlib import Table

ENTRY_TYPE = {'input': 1,
              'exit': 2, 
              'marker': 3,
              'timer': 4}

OPERATOR_TYPE = {')=': 1}

MAX_LINE = 50

NAME_LOGIC_FILE = 'pnl_logc.db'
NAME_INPUTS_FILE = 'pnl_inpt.db'
NAME_OUTPUTS_FILE = 'pnl_oupt.db'


def getArg():
    # Get name database from arguments command string
    arg_cmd = []

    for param in sys.argv:
        arg_cmd.append(param)

    if len(arg_cmd) <= 1:
        print('--> Error: At least one parametr must be present!\n-->        "db_viewer.py <path name to database>"')
        exit()

    return arg_cmd[1]


class Input():
    """
        Class Input - class contains information about the input of the fire panel

        Open interface:
            printInfo() - prints input information to the console
            findChildren() - finds depends output 
            printChildren() - prints children information
    """
    def __init__(self, panel, input_numeral, name=None, input_type=None, description=None, tab=''):
        self.__panel = panel
        self.__input_numeral = input_numeral
        self.__type = input_type
        self.__name = None
        self.__description = description 
        self.__children = {}
        self.__tab = tab

    def printInfo(self):
        print('* %s: %s {%s}' % (self.__input_numeral, self.__type, self.__description))

    def findChildren(self):

        table_operator = {')=': 1}
        status_find_child = False
        path_logic_file = self.__panel + '\\' + NAME_LOGIC_FILE

        with Table(path_logic_file) as inputs:

            for row in inputs: 
                if row['Line'] > 245:
                    break
                #print()
                #print(str(row['Par.0']), str(self.__input_numeral))
                #print(str(row['Opnd Num']), str(self.__type))
                print(row['Line'], str(row['Opnd Num']), str(self.__type))
                #print()
                if str(row['Par.0']) == str(self.__input_numeral) and \
                   str(row['Opnd Num']) == str(self.__type) and \
                   status_find_child == False:
                       print(str(row['Par.0']), str(self.__input_numeral))
                       print(str(row['Opnd Num']), str(self.__type))
                       print()
                       status_find_child = True

                if status_find_child == True and row['Optr Num'] == table_operator[')=']:
                    print(row['Line'], 'Number: ', row['Par.0'], row['Opnd Num'])
                    self.createChild(row['Par.0'], row['Opnd Num'])
                    status_find_child = False

    def createChild(self, numberchild, typechild):
        with Table(self.__panel + '\\' + NAME_INPUTS_FILE) as inputs:
            row = inputs[numberchild]
            self.__children[numberchild] = (typechild, \
                Input(self.__panel, '', numberchild, typechild, \
                    row['Input text'], '\t'))

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

    def printChildren(self):
        print('Function input.printChildren working.')
        print(self.__tab, self.__children)
        self.findChildrenOfChildren()


class Output():
    pass
                         

class Panel():
    # Class of database station
    def __init__(self, path):
        self._path = path
        self.path_logic_file = self._path + '\\' + NAME_LOGIC_FILE
        self.rows = []
        self.inputs = {} 
        self.outputs = {} 

        self.__getRowWithPanel()
        self.__getInputsInfo()
        self.__getOutputsInfo()
        
    def __del__(self):
        pass

    def __getRowWithPanel(self):
        with Table(self.path_logic_file) as logic_file:
            for row in logic_file:
                self.rows.append(row)

    def __getInputsInfo(self):

        with Table(self._path + '\\' + NAME_INPUTS_FILE) as inputs:
            for row in inputs:
                row_type = str(row['Type']).encode('cp850').decode('cp1251')
                row_input = str(row['Input']).encode('cp850').decode('cp1251')
                #print(type(row_input), row_input)
                row_description = str(row['Input text']).encode('cp850').decode('cp1251')
                if row_type not in ['Нет', 'None']:
                    pass
                    #print()
                    #print(row_input)
                    #print(row_type)
                    #print(row_description)
  
                if row_type in ['Нет', 'None']:
                    continue

                self.inputs[row_input] = [row_type, Input(self._path, row_input, row_type, 1, row_description)]


    def __getOutputsInfo(self):
        pass

    def printInfo(self):
        print()
        print('[ Fire panel info ]')
        print('* panel path: %s' % (self._path))
        print('* table: %s' % (self.path_logic_file))
        self.printInputs()
        print('* outputs: %s' % (self.outputs))

    def printInputs(self):
        for input in self.inputs.values():
            input[1].printInfo()

    def printRow(self, max_line = MAX_LINE):
        print(self.inputs)
        pass
        #for row in self.rows:
        #    if row['Line'] > max_line:
        #        break
#            if str(row['Operand']).encode('cp850').decode('cp1251') == 'Выход'.decode('cp1251'):
            #if str(row['Operand']).encode('cp850').decode('cp1251') == ''.encode('utf-8').decode('cp1251'):
                #print('РќР°Р№РґРµС‚ РІС…РѕРґ: ')
        #    print(str(row).encode('cp850').decode('cp1251'))

    def findInput(self, numberInput):
        print('Start function panel.findInput working.')
        print('numberInput: ', numberInput)
        print('numberInput type: ', type(numberInput))
        if type(numberInput) is not type(str):
            numberInput = str(numberInput)
        if numberInput in self.inputs:
            #print(self.inputs[str(numberInput)].findChildren())
            self.inputs[numberInput][1].findChildren()
            self.inputs[numberInput][1].printChildren()
        print('End of function panel.findInput working.')


class Database():
    def __init__(self, path):
        """
            Initialization Database
        """
        self._path = path
        self.work_dir = None

        self.panels_path = {}
        self.panels_db = {}

        self.__getPathToPanels()
        self.__getPanels()

    def __getPathToPanels(self):
        """
            Get paths of panels
        """
        db = Table(self._path) 

        self.work_dir = os.path.dirname(self._path)
        
        for panel in db:
            if panel['Panel Name'] is not None:
                panel_dir = self.work_dir + '\\' + panel['Panel Name']
                if os.path.exists(panel_dir):
                    self.panels_path[panel['Panel Name']] = panel_dir
        db.close

    def __getPanels(self):
        """
            Get db of panels 
        """
        print('~log~: getPanels function job')

        for (panel_name, panel_path) in self.panels_path.items():
            self.panels_db[panel_name] = Panel(panel_path) 

    def printDatabaseInfo(self):
        """ 
            Print station info 
        """ 
        print()
        print('dir of database: ', self.work_dir)

        for panel_name, panel_path in self.panels_path.items():
            print("Panel {name, path}: %s -> %s" % (panel_name, panel_path))

    def printPanelsInfo(self):
        """
            Print panels info
        """
        for (panel_name, panel_db) in self.panels_db.items():
            panel_db.printInfo()
            panel_db.printRow()

    def findInputFromPanel(self, panel, input):
        print('Function database.findInputFromPanel working.')
        self.panels_db[panel].findInput(input)    

    def __del__(self):
        pass


if __name__ == '__main__':
    pass
