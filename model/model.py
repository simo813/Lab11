import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.DAO = DAO()
        self.graphMO = None
        self.idMap = {}
        self._bestPathMO = []

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
                    if weight > 0:
                        graph.add_edge(prodotto1, prodotto2, weight=weight)
                else:
                    continue
        return graph

    def creaIdMap(self, graph):
        self.idMap = {}
        for node in list(graph.nodes()):
            self.idMap[node.Product_number] = node

    def getOptPath(self, sourceIDStr):
        """
        Trova il percorso più lungo a partire dal nodo identificato da sourceIDStr,
        con la condizione che il peso degli archi sia non decrescente.

        Args:
            sourceIDStr: L'ID del nodo di partenza della ricerca (stringa).

        Returns:
            list: Il percorso più lungo trovato, rappresentato come una lista di tuple
                  (nodo_inizio, nodo_fine, peso_arco).
        """
        self._bestPathMO = []
        source = self.idMap[int(sourceIDStr)]
        parziale = [source]
        miglior_percorso_globale = []

        vicini = list(self.graphMO.neighbors(source))
        if not vicini:
            return []

        for vicino in vicini:
            parziale.append(vicino)
            peso = self.graphMO[source][vicino]['weight']
            pathProvvisorio = [(source, vicino, peso)]
            percorso_trovato = self.ricorsione(parziale, pathProvvisorio, {source})  # Cambio nome variabile
            if len(percorso_trovato) > len(miglior_percorso_globale):
                print(f"\nmiglior percorso fin ora {len(percorso_trovato)}")
                miglior_percorso_globale = copy.deepcopy(percorso_trovato)
            parziale.pop()
        self._bestPathMO = miglior_percorso_globale
        lunghezzaBestPath = len(self._bestPathMO)
        return lunghezzaBestPath

    def ricorsione(self, parziale, pathProvvisorio, visited):
        """
        Funzione ricorsiva per esplorare i percorsi nel grafo, applicando il vincolo
        di peso non decrescente sugli archi.

        Args:
            parziale (list): Il percorso parziale corrente (lista di nodi).
            pathProvvisorio (list): La lista degli archi che compongono il percorso parziale corrente,
                             rappresentati come tuple (nodo_inizio, nodo_fine, peso_arco).
            visited (set): Insieme dei nodi visitati nel percorso corrente.

        Returns:
            list: Il percorso più lungo trovato in questa chiamata ricorsiva.
        """
        if len(parziale) < 2:
            return pathProvvisorio

        ultimo_nodo = parziale[-1]
        penultimo_nodo = parziale[-2]
        vicini = list(self.graphMO.neighbors(ultimo_nodo))
        miglior_percorso_locale = copy.deepcopy(pathProvvisorio)
        trovato_nodo_valido = False

        for node in vicini:
            peso_arco_corrente = self.graphMO[ultimo_nodo][node]['weight']
            peso_arco_precedente = self.graphMO[penultimo_nodo][ultimo_nodo]['weight']
            if self.rispettaVincoli(node, peso_arco_corrente, peso_arco_precedente, visited):
                trovato_nodo_valido = True
                nuovo_arco = (ultimo_nodo, node, peso_arco_corrente)
                pathProvvisorio.append(nuovo_arco)
                parziale.append(node)
                visited.add(node)
                percorso_candidato = self.ricorsione(parziale, pathProvvisorio, visited)
                if len(percorso_candidato) > len(miglior_percorso_locale):
                    miglior_percorso_locale = copy.deepcopy(percorso_candidato)
                parziale.pop()
                pathProvvisorio.pop()
                visited.remove(node)
        if not trovato_nodo_valido:
            return miglior_percorso_locale #ritorna il miglior percorso trovato, che potrebbe essere quello iniziale
        return miglior_percorso_locale

    def rispettaVincoli(self, node, peso_arco_corrente, peso_arco_precedente, visited):
        """
        Verifica se un nodo e il peso dell'arco corrente rispettano i vincoli.

        Args:
            node: Il nodo da controllare.
            peso_arco_corrente: Il peso dell'arco corrente.
            peso_arco_precedente: Il peso dell'arco precedente.
            visited (set): L'insieme dei nodi visitati.

        Returns:
            bool: True se il nodo e il peso dell'arco rispettano i vincoli, False altrimenti.
        """
        if peso_arco_corrente >= peso_arco_precedente and node not in visited:
            return True
        return False
