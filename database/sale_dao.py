from database.DB_connect import DBConnect
from model.sale import Sale


def get_years_from_DB():
    cnx = DBConnect.get_connection()
    if cnx is not None:
        cursor = cnx.cursor()
        query = """SELECT DISTINCT YEAR(gds.Date) FROM go_daily_sales gds"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result
    else:
        print("Errore di connessione")

def get_sales():
    cnx = DBConnect.get_connection()
    if cnx is not None:
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT gds.*
            FROM go_daily_sales gds"""
        cursor.execute(query)
        result = []
        for row in cursor:
            row_sale = Sale(row["Date"],
                            row["Quantity"],
                            row["Unit_price"],
                            row["Unit_sale_price"],
                            row["Retailer_code"],
                            row["Product_number"],
                            row["Order_method_code"])
            result.append(row_sale)
        cursor.close()
        cnx.close()
        return result
    else:
        print("Errore nella connessione")
        return None