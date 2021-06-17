#! python
# coding=utf=8

import sys
from pypxlib import Table

table_status = {1: 'Entry',
                2: 'Exit', 
                3: 'Marker',
                4: 'Timer'}

table_operator = {')=': 1}

arg_cmd = []

def Main():
    for param in sys.argv:
        arg_cmd.append(param)

    if len(arg_cmd) <= 1:
        print('*Error: At least one parametr must be present!\n*       "db_viewer.py <database file name>"')
        exit()

    #for (field, value) in table.fields.items():
    #    print(field, value)
    #print('\n', len(table), '\n')

    table = Table(arg_cmd[1])
    #table = Table('pnl_logc.db')

    # findExit(Name table, operator type, operator`s number)
    findExit(table, 1, 50)
            
    table.close

def findExit(table_find, opnd_num_find, par_find, tab = '', line = 0):
    
    tab = tab + '\t'
    find_entry = False

    print('\n', tab, '[->' , table_status[opnd_num_find].upper(), ':', par_find, ']')

    for row in table_find:
        if row['Line'] <= line: continue

        if row['Opnd Num'] == opnd_num_find and \
           row['Par.0'] == par_find and \
           find_entry == False:

            find_entry = True

        if find_entry == True:
            #find ')='
            if row['Optr Num'] == table_operator[')=']:

                status = 'None'

                if row['Opnd Num'] in table_status:
                    status = table_status[row['Opnd Num']]

                print(tab, '   ', row['Line'], ':', row['Par.0'], ':', status)
                find_entry = False

                if row['Opnd Num'] == 3 and \
                   par_find != row['Par.0']:
                    findExit(table_find, 3, row['Par.0'], tab, line = row['Line'])

                if row['Opnd Num'] == 4 and \
                   par_find != row['Par.0']:
                    findExit(table_find, 4, row['Par.0'], tab, line = row['Line'])
                     
    print(tab, '[<-', table_status[opnd_num_find].upper(), ':', par_find, ']\n')

def getArg():
    pass


if __name__ == '__main__':
    Main()
