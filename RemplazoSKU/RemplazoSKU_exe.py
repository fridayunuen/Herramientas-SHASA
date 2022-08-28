# El proposito de este programa es detectar el sku en el nombre de una foto he intercambiarlo conforme a 
# un documento excel 
import os
import pandas as pd
import time
# First, we select the path of the folder where the photos are stored

# FOTOS EN CARPETA --------------------------------------------------------------------------
path_fotos = r"C:\Users\fcolin\SERVICIOS SHASA S DE RL DE CV\Administrador - Fotografías Subir Pagina\Ropa Tendencias Otono Invierno 2019\Aventura Urbana"

# FOTOS EN EXCEL --------------------------------------------------------------------------
print("Leyendo el documento de cambio de items...")
df = pd.read_excel("Cambios.xlsx")

archivos_excel = pd.DataFrame(df.filename)
ls_items = os.listdir(path_fotos)
ls_items = os.listdir(path_fotos)

archivos_carpeta = pd.DataFrame({"filename" : ls_items})

fotos_carpeta_excel = pd.merge(archivos_excel, archivos_carpeta, on="filename", how="inner")
ls_items =fotos_carpeta_excel["filename"]


ls_items = pd.unique(ls_items)


ls_images = []
for item in ls_items:
    if item.endswith('.jpg') or item.endswith('.png'):
        # ls_images.append(item)
        #year = item[:2]
        #if int(year) < 20 and len(item) == 13:
        ls_images.append(item)

if ls_images == []:
    print("No hay fotos en la carpeta que coincidan con Cambios.xlsx")
    exit 
    
     
# Detetect wich character is a number
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
        for number in numbers:
            if len(number) >=10:
             #return number
                year = number[:2]
                if int(year) < 20 and len(number) == 13:
                    return number
                else:    
                    return 0
            else:   
                return 0       

colores = pd.read_excel('Copia de Mapeo de Colores y Tallas.xlsx', dtype=str)                


def nuevo_sku(item): 
    color_viejo = colores.COLOR[colores.COD== item[-3:]]
    color_viejo = color_viejo.to_string(index=False)
    nuevo_code = colores["NUEVO COD"][colores["NUEVO COLOR"] == color_viejo]
    # nuevo_code = str(set(nuevo_code))
    nuevo_code = pd.unique(nuevo_code)
    nuevo_code ="".join(nuevo_code)

    producto = item[:-6]
    color_anterior = item[-3:]
    talla = item[7:10]

    nueva_estructura = producto + color_anterior + talla
    sku_actual = producto + nuevo_code + talla
    
    return sku_actual

for j in range (len(ls_images)):
    item = extract_numbers(ls_images[j])

    color_viejo = colores.COLOR[colores.COD== item[-3:]]
    color_viejo = color_viejo.to_string(index=False)

    nuevo_code = colores["NUEVO COD"][colores["NUEVO COLOR"] == color_viejo]
    
    nuevo_code = pd.unique(nuevo_code)
    nuevo_code ="".join(nuevo_code)

    producto = item[:-6]
    color_anterior = item[-3:]
    talla = item[7:10]

    nueva_estructura = producto + color_anterior + talla
    sku_actual = producto + nuevo_code + talla


print("Renombrando SKUs indicados en el documento...")
reporte = []
for j in range(len(ls_images)):
    
    sku_viejo =  extract_numbers(ls_images[j])
    
    if sku_viejo != 0:
       
        sku_nuevo = nuevo_sku(extract_numbers(ls_images[j]))
        nuevo_nombre = ls_images[j].replace(sku_viejo, sku_nuevo)


        path_new_folder = os.path.join(path_fotos, 'Fotos_reemplazadas')
        if not os.path.exists(path_new_folder):
            os.makedirs(path_new_folder) 

        # get path of ls_images[j]
        old_path = os.path.join(path_fotos, ls_images[j])
        new_path = os.path.join(path_new_folder, nuevo_nombre)
        print(old_path)
        print(new_path)

        #date = os.path.getctime(old_path)
        #date = time.ctime(date)
    
        os.rename(old_path, new_path)
        #reporte.append([sku_viejo, sku_nuevo, ls_images[j], nuevo_nombre, date])
        reporte.append([sku_viejo, sku_nuevo, ls_images[j], nuevo_nombre])
        print("Renombrado realizado con exito "+sku_viejo+ " por " +sku_nuevo)

#creporte = pd.DataFrame(reporte, columns=["SKU VIEJO", "SKU NUEVO", "NOMBRE VIEJO", "NOMBRE NUEVO", "FECHA"])

reporte = pd.DataFrame(reporte, columns=["SKU VIEJO", "SKU NUEVO", "NOMBRE VIEJO", "NOMBRE NUEVO"])
reporte.to_excel("Reporte.xlsx", index=False)
print("Reporte impreso")


