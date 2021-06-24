#! python

import sys
#import db_viewer_lib
from libdb import *


def Main():
    print()

    name_fire_panel = getArg()

    database = Database(name_fire_panel)
    #database = Database(r"C:\bin\project\python\db_viewer\DB\26042021")

    database.printDatabaseInfo()

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


if __name__ == '__main__':
    Main()
