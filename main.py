import pandas as pd 
from api_interacction import GoogleSheet


#access credentials
file_name_gs = "pruebatecnica-440621-dd0bdadf72a1.json"
sheet = "data_prueba"
sheet_name="empleados"

#conection to sheets api
sheet = GoogleSheet(file_name_gs, sheet, sheet_name)
#get data
data = sheet.get_sheet_data()
#show data
print(data)
#get anual salary 
new_salary = sheet.get_anual_salary(data)
#add anual salary to dataframe
name = 'Salario Anual'
new_data = sheet.add_columntodf(data, new_salary,name)
#show new df
print(new_data)
#add column Años en la Empresa
name = 'Años en la Empresa'
total_years = sheet.get_years_by_employee(data)
new_data = sheet.add_columntodf(data, total_years,name)
#delete fecha de contratacion
new_data.drop(columns=['Fecha de Contratacion'], axis=1, inplace=True) 
sheet.write_data(new_data)
