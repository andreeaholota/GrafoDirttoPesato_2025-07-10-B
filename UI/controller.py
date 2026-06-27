import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._ddCategoryValue, self._view._dp1.value, self._view._dp2.value)
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {self._view._dp1.value.date()}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {self._view._dp2.value.date()}"))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{Nedges}"))
        self._fillDDProds()
        self._view.update_page()

    def handleBestProdotti(self,e):
        bestprodotti = self._model.getBestProdotti()
        self._view.txt_result.controls.append(ft.Text(f"I cinque prodotti più venduti sono:"))
        for p in bestprodotti:
            self._view.txt_result.controls.append(ft.Text(f"{p[0].product_name} with score {p[1]}"))
        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._view._txtInLun.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire lunghezza del cammino"))
            self._view.update_page()
            return
        try:
            lun = int(self._view._txtInLun.value)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Valore inserito non numerico"))
            self._view.update_page()
            return

        path, score = self._model.getBestPath(lun, self._ddProdStartValue, self._ddProdEndValue)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino migliore:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Score: {score}"))
        self._view.update_page()

    def fillDDCat(self):
        mycat = self._model.getCategories()
        catDDoptions = list(map(lambda y: ft.dropdown.Option(key=y.category_name,
                                                                  data=y,
                                                                  on_click=self._choiceCategory), mycat))
        self._view._ddcategory.options = catDDoptions

        self._view.update_page()

    def _choiceCategory(self, e):
        self._ddCategoryValue = e.control.data

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    def _fillDDProds(self):
        allNodes = self._model.getAllNodes()
        nodesDdOptionStart = list(map(lambda y: ft.dropdown.Option(key=y.product_name,
                                                                  data=y,
                                                                  on_click=self._choiceProdStart), allNodes))
        nodesDdOptionEnd = list(map(lambda y: ft.dropdown.Option(key=y.product_name,
                                                                  data=y,
                                                                  on_click=self._choiceProdEnd), allNodes))
        self._view._ddProdStart.options = nodesDdOptionStart
        self._view._ddProdEnd.options = nodesDdOptionEnd

        self._view.update_page()

    def _choiceProdStart(self, e):
        self._ddProdStartValue = e.control.data

    def _choiceProdEnd(self, e):
        self._ddProdEndValue = e.control.data