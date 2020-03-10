import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
import datetime
from tableausdk import *
from tableausdk.Extract import *
from tableausdk.Exceptions import *


#####DEPREACATED IF USING TABLEAu INSTEAD##
def exportToFile(fileName):
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "Time"
    return save_virtual_workbook(wb)

#send in dataseet
def to_tde(tde_name):
 
        # Step 1: Create the Extract File
        dataExtract = Extract("test1.tde")

        if dataExtract.hasTable('Extract'):
            return print("tde already exist use another name")

        # Step 2: Create the table definition
        dataSchema = TableDefinition()
        dataSchema.addColumn('Test1', Type.UNICODE_STRING)
        dataSchema.addColumn('Test2', Type.UNICODE_STRING)
    
        # Step 3: Create a table in the image of the table definition
        table = dataExtract.addTable('Extract', dataSchema)

        # Step 4: Create rows and insert them one by one
        newRow = Row(dataSchema)
        #for i in range(0, len(dataset)):
         #   #newRow.setString        (0, dataset['Station'][i])
        table.insert(newRow)

        # Step 5: Close the tde
        dataExtract.close()
        