import pandas as pd
import gspread 
from gspread_formatting import format_cell_range, CellFormat, NumberFormat
from datetime import datetime
from dateutil import relativedelta

class GoogleSheet:
    def __init__(self,file_name,document,sheet_name):
        self.gc = gspread.service_account(filename=file_name) #autorize credentials
        self.sh = self.gc.open(document) # open document
        self.sheet = self.sh.worksheet(sheet_name)  #open first worksheet
        self.new_worksheet = self.sh.add_worksheet(title="Reporte Salarios", rows="100", cols="20") #create new worksheet
        currency_format = CellFormat(
            numberFormat=NumberFormat(type="NUMBER", pattern="$#,##0.00") 
        )
        format_cell_range(self.new_worksheet, 'C:C', currency_format)
    
    def get_sheet_data(self):
         data = self.sheet.get_all_values()
         df = pd.DataFrame(data[1:], columns=data[0]) 
         return df
    

    def get_anual_salary(self, data):
       
       currency_format = CellFormat(
            numberFormat=NumberFormat(type="NUMBER", pattern="¤#,##0.00")  # ¤ para símbolo de moneda
)
       
       salary =  data['Salario Mensual'].astype(str).str.replace('$', '')
       salary =  salary.str.replace(',', '.')
       anual_salary = []
       for salario in salary: 
           new_salario = float(salario) * 12
           anual_salary.append(new_salario)
           new_salario = 0
       return anual_salary
    
    def get_years_by_employee(self, data):
        date_emp= data['Fecha de Contratacion'].astype(str)
        now = datetime.now()
        years =[]
        for year in date_emp:
            years_working = datetime.strptime(year, "%d/%m/%Y")
            total_time = relativedelta.relativedelta(now, years_working)
            years.append(total_time.years)
            total_time = 0
        return years


    def add_columntodf(self, data, column,name):
        data[name] = column
        return data

    def write_data(self, new_data):
       #write the new data
       self.new_worksheet.update([new_data.columns.values.tolist()] + new_data.values.tolist()) 
       