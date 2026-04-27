from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self):
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges2()

    def addEdges2(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u, v):
                    self._grafo.add_edge(u, v)

    def addEdges2(self):
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v =  self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges3(self):
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]

    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        pass

    @property
    def fermate(self):
        return self._fermate