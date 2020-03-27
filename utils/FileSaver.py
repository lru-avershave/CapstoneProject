import pandas as pd
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
import os.path
from io import BytesIO

def exportToFile():
    wb = Workbook()
    #sheet
    ws = wb.active
    ws.title = "INSERT A NUMBER HERE"

    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        str_io = BytesIO(tmp.read())
    return str_io
    