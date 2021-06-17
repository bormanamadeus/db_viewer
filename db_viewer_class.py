#! python

import sys
#import db_viewer_lib
from libdb import *


def Main():
    print()

    name_fire_panel = getArg()

    database = Database(r"C:\bin\project\python\db_viewer\DB\26042021\Pnl_info.db")

    database.printDatabaseInfo()
    database.printPanelsInfo()

    print()
    print('*** Start find input: ***')
    database.findInputFromPanel('Pnl_1', 1)

if __name__ == '__main__':
    Main()
