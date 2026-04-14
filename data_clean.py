# step 1 - data cleaning
import pandas as pd

def load_data():
    df = pd.read_csv('Product_Sales.csv')


    
    df = df.dropna() #drop null values
    df = df.drop_duplicates() #drop duplicates

    ##fixing all datatypes

    #changing the string dates to actual date objects
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'], errors='coerce')


    # all numeric columns to actual numbers, coercing errors to NaN
    numeric_cols = ['Quantity', 'UnitPrice', 'TotalPrice', 'Discount', 'ShippingCost']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    #for textual data
    #remove spce and make to title case
    df['Region'] = df['Region'].str.strip().str.title() 
    df['Product'] = df['Product'].str.strip().str.title()
    df['CustomerType'] = df['CustomerType'].str.strip().str.title()

    #remove errornous rows...so that there are no negative values
    df = df[df['Quantity'] >= 0]
    df = df[df['UnitPrice'] >= 0]

    df['ShippingDuration']=(df['DeliveryDate'] - df['OrderDate']).dt.days

    df['Profit'] = df['TotalPrice'] - (df['Quantity'] * df['UnitPrice'])

    #formula : totalprice - quantity * unitprice
    df['ProfitMargin'] = df['Profit'] / df['TotalPrice']

    return df





