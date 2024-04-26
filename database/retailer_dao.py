from database.DB_connect import DBConnect
from model.retailer import Retailer

def get_retailers_from_DB() -> set[Retailer] | None:
    cnx = DBConnect.get_connection()
    if cnx is not None:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM go_retailers")
        retailers = set()
        for row in cursor.fetchall():
            r = Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"])
            retailers.add(r)
        cursor.close()
        cnx.close()
        return retailers
    else:
        print("Errore di connessione")
        return None

# PRENDE SOLO IL RETAILER DEL PRODOTTO
@staticmethod
def get_retailer(product_code) -> Retailer | None:
        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT gr.*
                FROM go_retailers gr
                WHERE gr.retailer_code =%s"""
            cursor.execute(query, (product_code,))
            row = cursor.fetchone()
            row_retailer = Retailer(row["Retailer_code"],
                                    row["Retailer_name"],
                                    row["Type"],
                                    row["Country"])
            cursor.close()
            cnx.close()
            return row_retailer
        else:
            print("Errore nella connessione")
            return None


