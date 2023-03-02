import pandas as pd
import openpyxl

def format_worksheet(writer, sheet_name):
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 20)
    tech_format = writer.book.add_format({'bold': True, 'border': True, 'align': 'center'})
    worksheet.set_row(0, cell_format=tech_format)