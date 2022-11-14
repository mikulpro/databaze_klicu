from genExcel.gen_excel import ExcelGenerator
from sqlite.db_interface import Db


db = Db("sqlite:///sqlite/db.sqlite")


data = db.excel_dump()
ExcelGenerator.gen_excel_file(data, "export_14_11_2022.xlsx")
