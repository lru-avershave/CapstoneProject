import pandas as pd
from openpyxl import Workbook
import datetime
 
def exportToFile(fileName):
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "Time"
    wb.save(filename = fileName + ".xlsx")
