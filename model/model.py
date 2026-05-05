from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        # DIZIONARIO CHE POSSO INTERROGARE CON LA CHIAVE DI UNO DEI VALORI DI Connessione
        # (id_stazA) E RITORNA IL VALORE CORRISPOSNDENTE DELL'ALTRA datacalss Fermata

        # QUINDI E' UTILE PER RECUPERARE OGGETTI DATO IL LORO id (DI SOLITO UTILIZZIAMO chiave primaria)
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f


    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
        # RIUTILIZZARE IL PRINCIPIO DI FUNZIONAMENTO DEL METODO addEdges3,
        # MA CONTANDO QUANTE VOLTE PROVO AD AGGIUNGERE L'ARCO
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]

            # COSA TIPICA DA FARE QUANDO HO BISOGNO DI ARCHI PESATI, OPPURE
            # FARLO DIRETTAMENTE NEL DAO
            if self._grafo.has_edge(u, v):
                # GRAFO DEFINITO COME UN DIZIONARIO
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight = 1)

    def addEdgesPesati2(self):
        # DELEGA IL CALCOLO DEL PESO AD UNA QUERY SQL
        # PER SEMPLIFICARE CODICE PYTHON
        self._grafo.clear_edges()
        allEdgesWPeso = DAO.getAllEdgesPesati()

        for e in allEdgesWPeso:
            u = self._idMapFermate[e[0].id_stazP]
            v = self._idMapFermate[e[1].id_stazA]
            peso = e[2]
            self._grafo.add_edge()

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)

        edgesMaggiori =  []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                # self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori



    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        tic = datetime.now()
        self.addEdges3()
        tac = datetime.now()
        print(f"Tempo impiegato dal metodo 3: {tac - tic}")

# SE IL GRAFO E' PICCOLO, POSSO UTILIZZARE 2 CICLI for ANNIDATI,
# DATO CHE LA query IN SQL SARA' PIU' FACILE
    def addEdges(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u, v):
                    self._grafo.add_edge(u, v)

    def addEdges2(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v =  self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges3(self):
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

# ============================================================================================

    def getBFSNodesFromEdges(self, source):
        nodiBFS = []
        # ITERABLE DI TUPLE
        archi = nx.bfs_edges(self._grafo, source)
        for u, v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSNodesFromEdges(self, source):
        nodiDFS = []
        # ITERABLE DI TUPLE
        archi = nx.dfs_edges(self._grafo, source)
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

# ============================================================================================

    def get_numNodi(self):
        return len(self._grafo.nodes)

    def get_numArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate