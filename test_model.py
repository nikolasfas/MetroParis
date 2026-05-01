from model.fermata import Fermata
from model.model import Model

model = Model()
print(f"Numero di nodi: {model.get_numNodi()}")
print(f"Numero di archi: {model.get_numArchi()} ")
model.buildGraph()
print(f"Numero di nodi: ", (model.get_numNodi()))
print(f"Numero di archi: {model.get_numArchi()} ")


source = Fermata(2, "Abbesses", 2.33855, 48.8843)

nodiBFS = model.getBFSNodesFromEdges(source)

print(len(nodiBFS))
for i in range(0, 10):
    print(nodiBFS[i])

nodiDFS = model.getDFSNodesFromEdges(source)

print(len(nodiDFS))
for i in range(0, 10):
    print(nodiDFS[i])
