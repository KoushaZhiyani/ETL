import urllib
import pandas as pd
from sqlalchemy import create_engine, NVARCHAR

def read_table_from_sql(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df


def save_table_to_sql(df, table_name, if_exists='append'):
    """
    ذخیره دیتافریم در SQL Server
    پارامترها:
    df: دیتافریم مورد نظر
    table_name: نام جدول در دیتابیس
    if_exists: رفتار در صورت وجود جدول ('replace'، 'append'  'fail')

    """

    list_persain_str = ["Fact_Sell", "Fact_Return"]
    if table_name in list_persain_str:
        df.to_sql(name=table_name, con=engine, schema="dbo", index=False, if_exists=if_exists,     dtype={
            "invckind": NVARCHAR(80),
            "custname": NVARCHAR(200),
            "description": NVARCHAR(500)
        })

    elif table_name == "Dim_Custom":

        df.to_sql(name=table_name, con=engine, schema="dbo", index=False, if_exists=if_exists,     dtype={
            "name": NVARCHAR(200),
            "Customer_Group": NVARCHAR(500)
        })

    else:
        df.to_sql(name=table_name, con=engine, schema="dbo", index=False, if_exists=if_exists)

server = ''
database = ''


params = urllib.parse.quote_plus(
    f"DRIVER={};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

