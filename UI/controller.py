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
        self._view.txtOut.controls.clear()
        if self._view.ddColorValue != None and self._view.ddYearValue != None:
            graph = self._model.creaGrafo(self._view.ddColorValue, self._view.ddYearValue)
            stampa, listaTreArchiMaggiori = self.maxWeightEdges(graph)
            listaNodiPresentiInPiuArchi = self.nodiPresentiInPiuArchi(listaTreArchiMaggiori)
            self._view.txtOut.controls.append(ft.Text(f"numero di nodi: {graph.number_of_nodes()}, numero di archi: {graph.number_of_edges()}\n"
                                                      f"{stampa}\n"
                                                      f"I nodi ripetuti sono: {listaNodiPresentiInPiuArchi}"))
            self._view.btn_search.disabled = False
            for node in graph.nodes():
                self._view._ddnode.options.append(ft.dropdown.Option(key=node.Product_number, text=node.Product_number))

            self._view.update_page()
        else:
            self._view.txtOut.controls.append(
                ft.Text(f"seleziona i valori nelle dropdown"))
            self._view.update_page()


    def maxWeightEdges(self, graph):
        sorted_edges = sorted(graph.edges(data = True), key=lambda edge: edge[2]['weight'], reverse=True)
        listaTreArchiMaggiori = sorted_edges[:3]
        stampa = ""
        for arco in listaTreArchiMaggiori:
            stampa += f"Arco da {arco[0]} a {arco[1]}, peso {arco[2]['weight']}\n"
        return stampa, listaTreArchiMaggiori


    def nodiPresentiInPiuArchi(self, listaTreArchiMaggiori):
        listaNodiPresentiInPiuArchi = []
        listaNodi = set()
        for arco in listaTreArchiMaggiori:
            listaNodi.add(arco[0])
            listaNodi.add(arco[1])
        for nodo in listaNodi:
            contatore = 0
            for arco in listaTreArchiMaggiori:
                if nodo.Product_number == arco[0].Product_number or nodo.Product_number == arco[1].Product_number:
                    contatore += 1
            if contatore > 1:
                listaNodiPresentiInPiuArchi.append(nodo.Product_number)

        return listaNodiPresentiInPiuArchi


    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        sourceIDStr = self._view.ddNodeValue
        #print(source)  passa correttamente il codice nodo in stringa
        bestPathLenghtCO = self._model.getOptPath(sourceIDStr)
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {bestPathLenghtCO}"))
        self._view.update_page()

