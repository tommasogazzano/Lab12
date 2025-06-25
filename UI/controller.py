import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listCountry = self._model.getAllCountries()
        self._listYear = self._model.getAllYears()

        for n in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(n))

        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        self._view.update_page()



    def handle_graph(self, e):
        year = self._view.ddyear.value
        country = self._view.ddcountry.value
        if year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione selezionare anno!", color = "red"))
            self._view.update_page()
            return

        if country is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione selezionare nazione!", color = "red"))
            self._view.update_page()
            return



        self._model.buildGraph(country, year)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato con {nNodes} nodi e {nEdges} archi!", color="blue"))
        self._view.update_page()



    def handle_volume(self, e):
        tuple = self._model.getVolumiVendita()
        self._view.txtOut2.controls.clear()
        for e in tuple:
            self._view.txt_result.controls.append(ft.Text(f"{e[0].Retailer_name} --> {e[1]}"))

        self._view.update_page()




    def handle_path(self, e):
        pass
