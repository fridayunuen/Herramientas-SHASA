# El propósito de este es progrma es identificar sku coincidentes entre dos archivos de excel
# posteriormente buscar las fotos de los sku coincidentes en la página web de la empresa
# y extrarer su url

from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import re
import datetime as dt
import pyodbc
import pytz
from datetime import datetime, timedelta
import time
import os
import shutil
from selenium.webdriver.chrome.options import Options
import json
import random
import requests
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
import pandas as pd

BO  = pd.read_excel("BackOffice.xlsx", dtype = str)
BO["sku"] = BO["BackOffice"].str[:7]
BO.drop_duplicates(subset ="sku", keep = "first", inplace = True)
BO = BO[["sku", "BackOffice"]]

Faltates = pd.read_excel("ITems-Commerce.xlsx", dtype= str)
Faltates.columns = ["sku"]


# Coindidencias entre los dos archivos
df = pd.merge(Faltates, BO, on="sku", how="left")
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_excel("Coincidence.xlsx", index=False)

sku = df["sku"]
sku = sku.unique()

path_chromedriver = r'C:/Users/fcolin/AppData/Local/rasjani/WebDriverManager/bin/chromedriver.exe'

chrome_options = Options()

page_login = '''https://www.shasa.com''' 

driver = webdriver.Chrome(executable_path=path_chromedriver, options=chrome_options)
driver.get(page_login)
keyboard = Controller()

time.sleep(60)
print("OK")

df = pd.DataFrame({"sku":sku})
df["Link"] =  ""

for s in df["sku"]:
    print("Buscando... ", s) 
    time.sleep(2)
    driver.find_element(By.ID, 'js-site-search-input').send_keys(s)
    time.sleep(2)
    driver.find_element(By.ID, 'js-site-search-input').click()
    time.sleep(2)
    keyboard.press(Key.enter)
    time.sleep(2)

    html = driver.page_source
    two_tables_bs = BeautifulSoup(html, 'html.parser')
    table_rows = two_tables_bs.find_all("img")
    table_rows

    for row in table_rows:
        src = row.get('src')
        if src[:17] == "/medias/400Wx600H":
            # detect if sku is in the src
            if s in src:
                #print(s)
                print("https://www.shasa.com"+src)
                df.loc[df["sku"] == s, "Link"] = "https://www.shasa.com"+src
                break
        else: 
            df.loc[df["sku"] == s, "Link"] = "no"

        if src[35:50]=='missing_product':
            print("ProductoSinImagen")
            df.loc[df["sku"] == s, "Link"] = "ProductoSinImagen"
            break    
        

# Guardar el archivo en formato excel
df.to_excel("Links.xlsx", index=False)

    # 798m : 1543 productos
    #  91min: 438 productos
    #104 min:400 productos*
    #128m: 910 productos
    #489m: 3,468 productos
    #183min: 1,309 productos