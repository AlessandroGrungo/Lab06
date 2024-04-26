from database.DB_connect import DBConnect
from model.product import Product


def get_brands_from_DB():
    cnx = DBConnect.get_connection()
    if cnx is not None:
        cursor = cnx.cursor()
        cursor.execute('SELECT DISTINCT gp.Product_brand FROM go_products gp')
        brands = cursor.fetchall()
        cursor.close()
        cnx.close()
        return brands
    else:
        print("Errore di connessione")
        return None

#PRENDE SOLO IL PRODOTTO DI CUI CODICE E' PASSATO COME PARAMETRO
@staticmethod
def get_product(product_number):
    cnx = DBConnect.get_connection()
    if cnx is not None:
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT gp.* FROM go_products gp WHERE Product_number =%s"""
        cursor.execute(query, (product_number,))
        row = cursor.fetchone()
        row_product = Product(row["Product_number"],
                                    row["Product_line"],
                                    row["Product_type"],
                                    row["Product"],
                                    row["Product_brand"],
                                    row["Product_color"],
                                    row["Unit_cost"],
                                    row["Unit_price"])
        cursor.close()
        cnx.close()
        return row_product
    else:
        print("Errore nella connessione")
        return None