import os
import pandas as pd
import getpass

usuario = getpass.getuser()

drive= "C:/Users/"+usuario+"/SERVICIOS SHASA S DE RL DE CV/Fotos Shasa - Fotografía"
#drive = r"C:\Users\fcolin\SERVICIOS SHASA S DE RL DE CV\Fotos Shasa - Fotografía"

archivos = os.listdir(drive)

def extract_numbers(string):
    '''this function returns a list of numbers of one or more digits contained in a string
    '''
    numbers = []
    number = ''
    char_ant_isdigit = False
    for char in string:
        if char.isdigit() and char_ant_isdigit:
            number += char
        elif char.isdigit() and not char_ant_isdigit:
            number = char
        elif not char.isdigit() and char_ant_isdigit:
            numbers.append(number)
            number = ''
        char_ant_isdigit = char.isdigit()
    return numbers

def extract_item_number(string):
    '''this function returns the item number from a string
    the item number is a number contained in the string of lenght 10 or 13'''
    item_number = '0'
    for value in extract_numbers(string):
        if len(value) in [7, 10, 13]:
            item_number = value
    return item_number  


items= []
for archivo in archivos:   
    items.append(extract_item_number(archivo)) 

items = pd.unique(items)
# get hour of the system 

# Items Borrar
ib = pd.read_excel('ItemsBorrar.xlsx', dtype=str)  
items_borrar = pd.unique(ib.Items)


z = []
print("Eliminando...")
os.chdir(drive)
for j in range(len(items_borrar)):
    seleccion = items_borrar[j]
    print(seleccion)
    q = [items for items in items if seleccion in items]
    if len(q) > 0:
        for archivo in archivos:
            if q[0] in archivo:
                print(archivo)
                os.remove(archivo)
                z.append(archivo)


guardar = "C:/Users/" +usuario +"/Desktop"
os.chdir(guardar)
pd.DataFrame(z).to_excel("Resultados_BorrarItems.xlsx")
print("Reporte guardado en: " + guardar)

print("Se han eliminado " + str(len(z)) + " archivos")                