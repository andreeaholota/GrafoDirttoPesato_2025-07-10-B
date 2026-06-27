import networkx as nx
import copy
from database.DAO import DAO
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._products = []
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self, lungh, start, end):
        self._bestPath = []
        self._bestScore = 0
        parziale = [start]
        self._ricorsione(parziale, lungh, start, end)
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, lungh, start, end):
        if len(parziale) == lungh:
            if  parziale[-1] == end and self._getScore(parziale) > self._bestScore:
                self._bestScore = self._getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lungh, start, end)
                parziale.pop()

    def _getScore(self, parziale):
        score = 0
        for i in range(1, len(parziale)):
            score += self._graph[parziale[i-1]][parziale[i]]["weight"]
        return score

    def buildGraph(self, cat, date1, date2):
        self._graph.clear()
        self._products = DAO.getAllProductsbyCategory(cat)
        for p in self._products:
            self._idMap[p.product_id] = p

        self._graph.add_nodes_from(self._products)

        allEdges = DAO.getEdges(cat, date1, date2, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestProdotti(self):
        bestprodotti = []
        for n in self._graph.nodes:
            score = 0
            for e_out in self._graph.out_edges(n, data=True):
                score -= e_out[2]["weight"]
            for e_in in self._graph.in_edges(n, data=True):
                score += e_in[2]["weight"]

            bestprodotti.append((n, score))

        bestprodotti.sort(reverse=True, key=lambda x: x[1])
        return bestprodotti[0:5]

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCat()

    def getAllNodes(self):
        nodes = list(self._graph.nodes())
        nodes.sort(key = lambda x: x.product_name)
        return nodes