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
    print(database.getPanels()['Pnl_1'].getInputs()['1'].getChildren())

        #for (, input) in db.getOutputs().items():
        #    print('%s: %s: %s' % (number, input.getType(), input.getDescription()))


if __name__ == '__main__':
    Main()
