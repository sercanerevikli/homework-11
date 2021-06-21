import requests
import zipfile
import pandas


gdp_url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=csv"
unemployment_url = "https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv"
#it's an excel file
inflation_url = "https://filetransfer.io/data-package/NqlBwljO/download"
interest_url = "https://api.worldbank.org/v2/en/indicator/FR.INR.LEND?downloadformat=csv"

r1 = requests.get(gdp_url,allow_redirects=True)
r2 = requests.get(unemployment_url,allow_redirects=True)
r3 = requests.get(inflation_url,allow_redirects=True)
r4 = requests.get(interest_url,allow_redirects=True)

open("gdp.zip","wb").write(r1.content)
open("unemployment.zip","wb").write(r2.content) 
open("inflation.zip","wb").write(r3.content)
open("interest.zip","wb").write(r4.content)

with zipfile.ZipFile("gdp.zip","r") as zip_ref:
    zip_ref.extractall()

with zipfile.ZipFile("unemployment.zip","r") as zip_ref:
    zip_ref.extractall()

with zipfile.ZipFile("inflation.zip","r") as zip_ref:
    zip_ref.extractall()

with zipfile.ZipFile("interest.zip","r") as zip_ref:
    zip_ref.extractall()

for i in range(0,3):
    if i==1:
        csv = "API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_2445381.csv"
    elif i==2:
        csv = "API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_2445351.csv"
    else:
        csv = "API_FR.INR.LEND_DS2_en_csv_v2_2445736.csv"

    with open(csv, "r") as file:
        lines = file.readlines()
    del lines[:4]

    with open(csv, "w+") as file:
        for line in lines:
            file.write(line)


gdp_data = pandas.read_csv("API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_2445381.csv")
unemployment_data = pandas.read_csv("API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_2445351.csv")
inflation_data = pandas.read_excel("Inflation.xlsx")
interest_data = pandas.read_csv("API_FR.INR.LEND_DS2_en_csv_v2_2445736.csv")

year_list = list(inflation_data[inflation_data.columns.ravel()[0]][5:34])
gdp_list = list(gdp_data.iloc[99].ravel()[35:-2])
unemployment_list = list(unemployment_data.iloc[99].ravel()[35:-2])
inflation_list = list(inflation_data[inflation_data.columns.ravel()[2]][5:34])
interest_list = list(interest_data.iloc[99].ravel()[35:-2])


df = pandas.DataFrame({"Unemployment": unemployment_list,
                       "Inflation": inflation_list,
                       "Interest": interest_list,
                       "GDP":gdp_list}, index =year_list)

df["HAMI"] = df["Unemployment"] + df["Inflation"] + df["Interest"] - df["GDP"]



df.to_excel("HW11.xlsx")
