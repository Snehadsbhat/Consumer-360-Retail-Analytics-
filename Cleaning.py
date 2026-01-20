import pandas as pd
import numpy as np

df = pd.read_csv("online_retail.csv")
df.head()
df.info()
df.isnull().sum()
df['InvoiceDate'] = pd.to_datetime(
    df['InvoiceDate'],
    format='%d-%m-%Y %H:%M',
    errors='coerce'
)
df = df.dropna(subset=['InvoiceDate'])
df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
df.info()
df.describe()
df.to_csv("online_retail_cleaned_pandas.csv", index=False)
