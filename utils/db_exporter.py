import pyodbc
import pandas as pd

def export_sql_to_csv(filename="receipt_data.csv"):
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=receipt-db-server.database.windows.net;"
        "Database=ReceiptDB;"
        "Uid=receiptadmin;"
        "Pwd=Raceway4;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
  )
    query = "SELECT * FROM Receipts;"  # change to dbo.ReceiptItems if needed
    df = pd.read_sql(query, conn)
    df.to_csv(filename, index=False)
    conn.close()
    return filename