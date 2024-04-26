import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.anno = None
        self.brand = None
        self.retailer = None


    def read_anno(self, e):
        self.anno = e.control.data

    def popola_anno(self):
        anni = self._model.get_years()
        for anno in anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(key=anno[0], text=anno[0],
                                              data=anno[0], on_click=self.read_anno))
        self._view.update_page()

    def read_brand(self, e):
        if e.control.value is None:
            self.brand = None
        else:
            self.brand = e.control.value

    def popola_brand(self):
        brands = self._model.get_brands()
        for brand in brands:
            self._view.dd_brand.options.append(ft.dropdown.Option(brand[0]))
        self._view.update_page()

    def read_retailer(self, e):
        self.retailer = e.control.data

    def popola_retailer(self):
        retailers = self._model.get_retailers()
        for retailer in retailers:
            self._view.dd_retailer.options.append(ft.dropdown.Option(key=retailer.retailer_code,
                                                                  data=retailer,
                                                                  text=retailer.retailer_name,
                                                                  on_click=self.read_retailer))
        self._view.update_page()

    def handle_top_vendite(self,e):
        # INIZIATA OPERAZIONE INSERISCO IL CERCHIO DI CARICAMENTO
        self._view.pr_ring.visible = True
        self._view.btn_top_vendite.disabled = True
        self._view.btn_analizza_vendite.disabled = True
        self._view.update_page()
        #
        # TROVO LE TOP VENDITE PASSANDO IL PROBLEMA AL MODEL
        top_vendite = self._model.get_top_sales(self.anno, self.brand, self.retailer)
        # FINITA OPERAZIONE LEVO IL CERCHIO DI CARICAMENTO
        self._view.pr_ring.visible = False
        self._view.btn_top_vendite.disabled = False
        self._view.btn_analizza_vendite.disabled = False
        #
        # PULISCO I PRECEDENTI RISULTATI
        self._view.lst_result.controls.clear()
        # SE NE HO ZERO NON HO VENDITE CON TALI FILTRI
        if len(top_vendite) == 0:
            self._view.lst_result.controls.append(ft.Text("Nessuna vendita con i filtri selezionati"))
        else: # ALTRIMENTI STAMPO LE VENDITE NELLA LISTA FORMATA GIA' DA SOLO 5 VENDITE
            for vendita in top_vendite:
                self._view.lst_result.controls.append(ft.Text(vendita))
        self._view.update_page()


    def handle_analizza_vendite(self, E):
        # INIZIATA OPERAZIONE MOSTRO IL CERCHIO DI CARICAMENTO
        self._view.pr_ring.visible = True
        self._view.btn_top_vendite.disabled = True
        self._view.btn_analizza_vendite.disabled = True
        self._view.update_page()
        # TROVO LE STATISTICHE DELLE VENDITE PASSANDO I PARAMETRI AD UNA FUNZIONE DI MODEL
        # (OTTENGO UNA LISTA DI VENDITE CHE NON POSSO PRENDERE COME FOSSERO DIZIONARI MA COME ARRAY)
        statistiche_vendite = self._model.get_sales_stats(self.anno, self.brand, self.retailer)
        # FINITA OPERAZIONE NASCONDO IL CERCHIO DI CARICAMENTO
        self._view.pr_ring.visible = False
        self._view.btn_top_vendite.disabled = False
        self._view.btn_analizza_vendite.disabled = False
        # PULISCO L'OUTPUT
        self._view.lst_result.controls.clear()
        # IMPOSTO LA STRUTTURA DELL'OUTPUT
        self._view.lst_result.controls.append(ft.Text("Satistiche vendite:"))
        self._view.lst_result.controls.append(ft.Text(f"Giro d'affari: {statistiche_vendite[0]}"))
        self._view.lst_result.controls.append(ft.Text(f"Numero vendite: {statistiche_vendite[1]}"))
        self._view.lst_result.controls.append(ft.Text(f"Numero retailers coinvolti: {statistiche_vendite[2]}"))
        self._view.lst_result.controls.append(ft.Text(f"Numero prodotti coinvolti: {statistiche_vendite[3]}"))
        self._view.update_page()