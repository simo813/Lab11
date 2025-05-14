import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []


    def fillDD(self):
        self._view._ddyear.options.append(ft.dropdown.Option(key="2015", text="2015"))
        self._view._ddyear.options.append(ft.dropdown.Option(key="2016", text="2016"))
        self._view._ddyear.options.append(ft.dropdown.Option(key="2017", text="2017"))
        self._view._ddyear.options.append(ft.dropdown.Option(key="2018", text="2018"))
        listaColoriCO = self._model.passaColoriMO()
        for colore in listaColoriCO:
            self._view._ddcolor.options.append(ft.dropdown.Option(key=colore, text=colore))
        self._view.update_page()



    def handle_graph(self, e):
        graph = nx.Graph()
        listaNodi = self._model.cercaNodiMO(self._view._ddColorValue)
        listaArchi = self._model.cercaArchiMO(self._view._ddYearValue)
        graph.add_nodes_from(listaNodi)
        graph.add_edges_from(listaArchi)




    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
