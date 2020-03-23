import pandas as pd
from openpyxl import Workbook
import os.path


def exportToFile(fileName):

    name = fileName + ".xlsx"
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "INSERT A NUMBER HERE"

    #DO SOME DATA STUFF
    wb.save(name)
    if not os.path.isfile('FileName.xlsx'):
        wb.save(os.path.join('app//temporaryFiles', name))
    return wb