import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.dd_anno = None
        self.dd_brand = None
        self.dd_retailer = None
        self.btn_top_vendite = None
        self.btn_analizza_vendite = None
        self.pr_ring = None # anello di caricamento
        self.lst_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with dd
        self.dd_anno = ft.Dropdown(width=200,
                                   label="anno",
                                   hint_text="imposta filtro per anno",
                                   options=[ft.dropdown.Option(data=None,
                                                               text="Nessun filtro",
                                                               on_click=self._controller.read_anno)])
        self._controller.popola_anno()

        self.dd_brand = ft.Dropdown(width=200,
                                   label="brand",
                                   hint_text="imposta filtro per brand",
                                   options=[ft.dropdown.Option(key="None", text="Nessun filtro")],
                                                               on_change=self._controller.read_brand)
        self._controller.popola_brand()

        self.dd_retailer = ft.Dropdown(width=500, label="retailer", hint_text="imposta filtro per retailer",
                                       options=[ft.dropdown.Option(data=None,
                                                                   text="Nessun filtro",
                                                                   on_click=self._controller.read_retailer)])
        self._controller.popola_retailer()

        row1 = ft.Row([self.dd_anno, self.dd_brand, self.dd_retailer],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)

        # button
        self.btn_top_vendite = ft.ElevatedButton(text="Top Vendite",
                                                 on_click=self._controller.handle_top_vendite)
        self.btn_analizza_vendite = ft.ElevatedButton(text="Analizza Vendite",
                                                      on_click=self._controller.handle_analizza_vendite)
        # cerchio di caricamento
        self.pr_ring = ft.ProgressRing()
        self.pr_ring.visible = False  # lo decido io quando farlo vedere

        row2 = ft.Row([self.btn_top_vendite, self.pr_ring, self.btn_analizza_vendite],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row2)

        # List View where the reply is printed
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.lst_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
