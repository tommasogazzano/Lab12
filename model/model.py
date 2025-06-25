import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._listRetailer = []
        self._idMap = {}

    def getAllCountries(self):
        return DAO.getCountries()

    def getAllYears(self):
        return DAO.getYears()

    def getNodes(self, nation):
        self._listRetailer =  DAO.getRetailers(nation)
        for r in self._listRetailer:
            self._idMap[r.Retailer_code] = r
        return self._listRetailer

    def buildGraph(self, nation, anno):
        self._graph.clear()

        self.getNodes(nation)

        if len(self._listRetailer) == 0:
            print("No retailers found")
            return

        self._graph.add_nodes_from(self._listRetailer)
        self.addAllEdges(anno, nation, self._idMap)

    def addAllEdges(self, anno, nation, idMap):
        allEdges = DAO.getEdges(anno,nation, idMap)
        for edge in allEdges:
            self._graph.add_edge(edge[0], edge[1], weight=edge[2])

    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._graph.nodes())} nodi e {len(self._graph.edges())} archi")

    def getGraphDetails(self):
        return len(self._graph.nodes()), len(self._graph.edges())


    def getVolumiVendita(self):
        listaTuple = []
        for nodo, peso in self._graph.degree(weight='weight'):
            if peso > 0:
             listaTuple.append((nodo, peso))

        listaTuple.sort(key = lambda x: x[1], reverse = True)

        return listaTuple
