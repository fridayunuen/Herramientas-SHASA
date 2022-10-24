import pandas as pd

print("Leyendo Cubo....")
Cubo = pd.read_excel("Cubo.xlsx")

nombres = Cubo.iloc[18,:].values
Cubo = Cubo.iloc[19:,:]
Cubo.columns = nombres

Cubo = pd.DataFrame(Cubo["Item Variant"])

Cubo["sku"] = Cubo["Item Variant"].str[0:7]

Cubo["Item"] = Cubo["Item Variant"].str[0:10]

items = pd.read_excel("SKU_Productos.xlsx")

Product = []
for producto in items["Items"]:
    producto = str(producto)
    df = Cubo[Cubo["sku"] == producto]
    Item_ = df["Item"].str[0:7]+"_"+df["Item"].str[7:10]
    # df["Item_"] = df["Item"].str[0:7]+"_"+df["Item"].str[7:10]
    ItemVariant_ = df["Item Variant"].str[0:7]+"_"+df["Item Variant"].str[7:]
    #df["ItemVariant_"] = df["Item Variant"].str[0:7]+"_"+df["Item Variant"].str[7:]
    Categ = df['sku'].astype(str) + ', ' + Item_ + ', ' + ItemVariant_+", "
    categoria = Categ.to_list()
    #df["Categ"] = df['sku'].astype(str) + ', ' + df['Item_'].astype(str) + ', ' + df['ItemVariant_'].astype(str)+", "
    #categoria = df["Categ"].to_list()
    Product.append(''.join(categoria))

Product = ''.join(Product)

# send Producto to a text file
with open('Product.txt', 'w') as f:
    f.write(Product)
