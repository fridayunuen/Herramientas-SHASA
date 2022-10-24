FROM = r"C:/Users/fcolin/SERVICIOS SHASA S DE RL DE CV/Administrador - Fotografías Subir Pagina/CONNECT HISTORICO"
TO = r"C:\Users\fcolin\SERVICIOS SHASA S DE RL DE CV\Administrador - Fotografías Subir Pagina\CONNECT\TODOS_LOS_TAMANOS"

with open("path.txt", "w") as file:
    file.write(FROM)

import aux_mapping_items

import pandas as pd
import os

Mapping = pd.read_csv('Mapping.csv')
ItemsMover = pd.read_excel('ItemsMover.xlsx')

coincidencias = pd.merge(ItemsMover,Mapping , on='sku', how='left')

coincidencias = coincidencias[['sku','path','filename']]
coincidencias = coincidencias.dropna()
coincidencias

for index in coincidencias.index:
    sku = coincidencias['sku'][index]
    path = coincidencias['path'][index]
    filename = coincidencias['filename'][index]
    print("Moviendo...", filename)
    #print(FROM + path+r'\\'+filename)
    #print(TO +r'\\'+filename)
    if not os.path.exists(TO +r'\\'+filename):
        os.rename(FROM + path+r'\\'+filename, TO +r'\\'+filename)
    #os.rename(path+\\''+filename, TO+'\\'+filename)