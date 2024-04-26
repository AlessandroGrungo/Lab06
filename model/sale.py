from dataclasses import dataclass
import datetime
from database import retailer_dao, product_dao


@dataclass
class Sale:
    date: datetime.date
    quantity: int
    unit_price: float
    unit_sale_price: float
    # relazioni
    retailer_code: int
    product_number: int
    order_method_code: int
    retailer: retailer_dao.Retailer = None # May be needed later
    product: product_dao.Product = None # May be needed later

    # ricavo: campo non presente nel database, ma che aggiungo per comodità,
    # calcolandolo nel __post_init__(), ovverosia dopo che gli attributi principali sono già
    # stati popolati
    def __post_init__(self):
        self.ricavo: float = self.unit_sale_price * self.quantity

    # SERVE PER SCRIVERE SEMPLICEMENTE vendita.__str__ E AVERE SUBITO L'OUTPUT PRONTO
    def __str__(self):
        return f"Data: {self.date}; Ricavo: {self.ricavo}; Retailer: {self.retailer_code}; Product: {self.product_number}"

    """def __eq__(self, other):
        return (self.retailer_code == other.retailer_code
                and self.product_number == other.product_number
                and self.order_method_code == other.order_method_code)"""

    def __hash__(self):
        return hash((self.retailer_code, self.product_number, self.order_method_code))

    # FA IL CONFRONTO TRA OGGETTI PER ORDINARLI NELLE LISTE
    def __lt__(self, other):
        return self.ricavo < other.ricavo

    # ESTRAPOLA SOLO L'ANNO DALLA DATA (CON .year PERCHE' E' UN OGGETTO DATA)
    def get_year(self) -> int:
        return self.date.year

    # PRENDE IL RETAILER DA RETAILER_DAO SE ANCORA NON E' STATO PRESO
    def get_retailer(self):
        if self.retailer is None:
            self.retailer = retailer_dao.get_retailer(self.retailer_code)
        return self.retailer

    # PRENDE IL BRAND DA PRODUCT_DAO SE ANCORA NON E' STATO PRESO
    def get_brand(self) -> str:
        if self.product is None:
            self.product = product_dao.get_product(self.product_number)
        return self.product.product_brand
