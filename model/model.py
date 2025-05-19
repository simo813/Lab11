from UI.controller import Controller
from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.DAO = DAO()
        self.graphMO = None
        self.idMap = {}
        self._cost = 0
        self._bestPath = []


    def creaGrafo(self, colore, anno):
        self.graphMO = None
        graph = nx.Graph()
        listaNodi = self.cercaNodiMO(colore)
        graph.add_nodes_from(listaNodi)
        graph = self.cercaArchiMO(graph, anno)
        self.graphMO = graph
        self.creaIdMap(graph)
        return graph

    def passaColoriMO(self):
        listaColoriMO = self.DAO.getColors()
        return listaColoriMO

    def cercaNodiMO(self, color):
        listaNodi = self.DAO.getProductsOfColor(color)
        return listaNodi

    def cercaArchiMO(self, graph, anno):
        for prodotto1 in graph:
            for prodotto2 in graph:
                if prodotto1.Product_number > prodotto2.Product_number:
                    weight = self.DAO.getConnections(anno, prodotto1, prodotto2)
                    if  weight > 0:
                        graph.add_edge(prodotto1, prodotto2, weight = weight)
                else:
                    continue
        return graph

    def creaIdMap(self, graph):
        self.idMap = {}
        for node in list(graph.nodes()):
            self.idMap[node.Product_number] = node


    def getOptPath(self, source):
        self._bestPath = []
        self._cost = 0
        parziale = [source]
        for node in self.graphMO.neighbors(source):
            parziale.append(node)
            costoProvvisorio = 0
            costoProvvisorio += self.graphMO[source][node]['weight']
            self.ricorsione(parziale, costoProvvisorio)
            if costoProvvisorio > self._cost:
                self._cost = costoProvvisorio
            parziale.pop()

        return self._bestPath, self._cost


    def ricorsione(self, parziale, costoProvvisorio):
        for node in self.graphMO.neighbors(parziale[1]):
            if self.graphMO.edge[parziale[0], node] >= costoProvvisorio and parziale[1].__eq__(node) == False:
                parziale.pop(0)
                parziale.append(node)
                costoProvvisorio += self.graphMO[parziale[0]][node]['weight']
                self.ricorsione(parziale, costoProvvisorio)
                parziale.pop()














