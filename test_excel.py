from modules.excel_reader import ExcelReader

reader = ExcelReader()

reader.load("Excel/Terminefussball_2026_Herbst.xlsx")

print(reader.statistik())