from database import sale_dao, product_dao, retailer_dao


class Model:
    def __init__(self):
        self._sales_list = sale_dao.get_sales()

    def get_years(self):
        return sale_dao.get_years_from_DB()

    def get_brands(self):
        return product_dao.get_brands_from_DB()

    def get_retailers(self):
        return retailer_dao.get_retailers_from_DB()

    def get_top_sales(self, anno, brand, retailer):
        # TROVO LA LISTA FILTRATA PASSANDO IL PROBLEMA A UNA FUNZIONE APPOSTA
        filtered_sales = self.get_filtered_sales(anno, brand, retailer)
        # ORDINO LA LISTA IN ORDINE DECRESCENTE
        filtered_sales.sort(reverse=True)
        # PRENDO I PRIMI 5 (I TOP 5)
        return filtered_sales[0:5]

    def get_filtered_sales(self, anno, brand, retailer):
        # LISTA CHE CONTERRA' LE VENDITE CON TALI FILTRI
        filtered_sales = []
        # UTILIZZO LA LISTA DELLE VENDITE CHE INIZIALIZZO ALL'INIZIO
        # TRAMITE UNA FUNZIONE APPOSITA CHE LE PRELEVA DA SALE_DAO
        for listed_sale in self._sales_list:
            # LE FILTRO CONSIDERANDO ANCHE L'EVENIENZA IN CUI I PARAMETRI DEI FILTRI SIANO NONE
            if ((anno is None or listed_sale.get_year() == anno)
                    and (brand is None or listed_sale.get_brand() == brand)
                    and (retailer is None or listed_sale.get_retailer() == retailer)):
                filtered_sales.append(listed_sale)
        return filtered_sales

    def get_sales_stats(self, anno, brand, retailer):
        # PRELEVO LA LISTA COL METODO CHE FILTRA
        filtered_sales = self.get_filtered_sales(anno, brand, retailer)
        # SOMMO I RICAVI DI OGNI VENDITA PRESENTE NELLA LISTA OTTENUTA
        ricavo_totale = sum([sale.ricavo for sale in filtered_sales])
        # INSERISCO IN UN INSIEME I VENDITORI E I PRODOTTI PRESENTI NELLA LISTA
        retailers_involved = set([sale.retailer_code for sale in filtered_sales])
        product_involved = set([sale.product_number for sale in filtered_sales])
        return ricavo_totale, len(filtered_sales), len(retailers_involved), len(product_involved)