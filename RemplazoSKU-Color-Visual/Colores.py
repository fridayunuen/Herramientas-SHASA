# Librerias ----------------------------
import os
from tkinter import Tk, filedialog
from numpy import repeat
import cv2
from win32con import (SW_SHOW, SW_RESTORE)
import win32gui
import win32ui
import shutil
import zipfile
import datetime
import pandas as pd
import shutil

# Funciones|---------------------------- 
def get_windows_placement(window_id):
    return win32gui.GetWindowPlacement(window_id)[1]

def set_active_window(window_id):
    if get_windows_placement(window_id) == 2:
        win32gui.ShowWindow(window_id, SW_RESTORE)
    else:
        win32gui.ShowWindow(window_id, SW_SHOW)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)

    
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


# Filtrando solo que se busca cambiar ----------------------------
ItemsDuda = pd.read_excel("ItemsDuda.xlsx")
# Excel con el que se compararán los códigos ----------------------------
colores = pd.read_excel('Colores.xlsx', dtype=str)   

# Comenzando a leer los archivos de la carpeta seleccionada ----------------------------
carpeta = r"C:\Users\fcolin\Desktop\Prueba"
os.chdir(carpeta)
imagenes_carpeta = os.listdir()

no_codigo_color = []
item_no_encontrado = []
item_cambio = []

for j in range(len(ItemsDuda)):
    # Seleccionando todas las imagenes con el mismo sku ----------------------------
    #  Producto que coincide con la lista en excel
    item_carpeta= list(ItemsDuda["Items"])[j]
    item_carpeta = str(item_carpeta)
    item = [imagenes_carpeta for imagenes_carpeta in imagenes_carpeta if item_carpeta in imagenes_carpeta]
    

    #######################if
    if item == []:
        item_no_encontrado.append(item_carpeta)
        print(item_carpeta + " No esta en carpeta")
    else:      
        
        item_imprimir = [item for item in item if "515Wx515" in item][0]

        # Buscando el sku y codigos de color ----------------------------

        sku = extract_item_number(item[0])
        codigo_color_imagen = sku[-3:]
        color_imagen = colores.COLOR[colores.COD== codigo_color_imagen]
        color_imagen = color_imagen.to_string(index=False)

        color_excel = colores[colores["NUEVO COD"]== codigo_color_imagen]["NUEVO COLOR"]
        color_excel = pd.unique(color_excel)[0]
    
        codigo_color_excel = colores["NUEVO COD"][colores["NUEVO COLOR"] == color_excel]
        codigo_color_excel = pd.unique(codigo_color_excel)[0]
        # codigo_color_excel = codigo_color_excel.to_string(index=False)

        mensaje = color_excel+" = Si       "+ color_imagen+" = No"

        # Mostrando la imagen ----------------------------
        os.chdir(carpeta)
        img = cv2.imread(item_imprimir)
        cv2.imshow(sku,img) #
        cv2.setWindowProperty(sku, cv2.WND_PROP_TOPMOST, 1)
        window_id = win32gui.GetActiveWindow()
        set_active_window(window_id)
        # cv2.waitKey(0)
        seleccion = win32ui.MessageBox(mensaje, sku, 4) #SI =6 NO =7
        cv2.destroyAllWindows()

        # Realizando cambio de color ----------------------------

        if seleccion == 7:
            
            codigo_nuevo = colores["NUEVO COD"][colores["NUEVO COLOR"]==color_imagen]
            
            if codigo_nuevo.empty:
                no_codigo_color.append(sku)
                if not os.path.exists("No_cambio_color"):
                    os.makedirs("No_cambio_color")
                for image in item:
                    shutil.move(image, "No_cambio_color")    
                print(sku+" sin codigo para realizar cambio")
                break
            else:
                item_cambio.append(sku)

            codigo_nuevo = pd.unique(codigo_nuevo)[0]
            print(codigo_nuevo)

            sku_nuevo = sku.replace(codigo_color_imagen, codigo_nuevo)
            print(sku_nuevo)
            if not os.path.exists("Correcciones"):
                os.makedirs("Correcciones")

            for image in item:
                image_nueva = image.replace(sku, sku_nuevo)
                nuevo_nombre = os.path.join(carpeta,"Correcciones" ,image_nueva)
                os.rename(image, nuevo_nombre)
            
            print(sku + " cambiado a " + sku_nuevo)


item_cambio = pd.DataFrame(item_cambio)
item_cambio.to_excel("item_cambio.xlsx", index=False)
no_codigo_color = pd.DataFrame(no_codigo_color)
no_codigo_color.to_excel("No_cambio_color.xlsx", index=False)
item_no_encontrado = pd.DataFrame(item_no_encontrado)
item_no_encontrado.to_excel("Item_no_encontrado.xlsx", index=False)