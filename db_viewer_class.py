#! python

import sys

import menu


def Main():
    print()

    _menu = menu.Menu()
    _menu.mainloop() 

'''
    for (output_number, output) in database.getPanels()['Pnl_1'].getOutputs().items():
        print('%s: %s: %s' % (output_number, output.getType(), output.getDescription()))

    database.getPanels()['Pnl_1'].getInputs()['1'].findChildren()
    for ((number, etype), child) in database.getPanels()['Pnl_1'].getInputs()['1'].getChildren().items():
        print('%s\t%s\t%s' % (number, etype, child))
        if etype == 3:
            print('\t', database.getPanels()['Pnl_1']
                                .getInputs()['1']
                                .getChildren()[(number, etype)])

            database.getPanels()['Pnl_1']\
                    .getInputs()['1']\
                    .getChildren()[(number, etype)].findChildren()

            print('type: ', database.getPanels()['Pnl_1']\
                    .getInputs()['1']\
                    .getChildren()[(number, etype)].getType())

        #for (, input) in db.getOutputs().items():
        #    print('%s: %s: %s' % (number, input.getType(), input.getDescription()))
'''


if __name__ == '__main__':
    Main()
