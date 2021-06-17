#! python
# coding=utf=8

from pypxlib import Table

table_status = {1: 'Enter',
                2: 'Exit', 
                3: 'Marker',
                4: 'Timer'}
def Main():
    #for (field, value) in table.fields.items():
    #    print(field, value)
    #print('\n', len(table), '\n')

    table = Table('pnl_logc.db')

    find_exit(table, 1, 50)
            
    table.close

def find_exit(table_find, opnd_num_find, par_find, tab = '', line = 0):
    
    tab = tab + '\t'

    table_operator = {')=': 1}

    find_entry = False

    print('\n', tab, '[->' , table_status[opnd_num_find].upper(), ':', par_find, '->')

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

                print(tab, '   ', row['Line'], '\t:', row['Par.0'], '\t:', status)
                find_entry = False

                if row['Opnd Num'] == 3 and \
                   par_find != row['Par.0']:
                    find_exit(table_find, 3, row['Par.0'], tab, line = row['Line'])

                if row['Opnd Num'] == 4 and \
                   par_find != row['Par.0']:
                    find_exit(table_find, 4, row['Par.0'], tab, line = row['Line'])
                     
    print(tab, '<- ', table_status[opnd_num_find].upper(), ':', par_find, '<-]', '\n')

if __name__ == '__main__':
    Main()
