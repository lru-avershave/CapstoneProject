import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
import datetime
 
def exportToFile(fileName):
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "Time"
    return save_virtual_workbook(wb)
