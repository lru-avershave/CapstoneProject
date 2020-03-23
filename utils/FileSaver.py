import pandas as pd
from openpyxl import Workbook

def exportToFile(fileName):

    name = fileName + ".xlsx"
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "INSERT A NUMBER HERE"

    #DO SOME DATA STUFF
    wb.save(name)
    return wb