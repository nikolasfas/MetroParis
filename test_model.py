from model.model import Model

model = Model()
print(f"Numero di nodi: {model.get_numNodi()}")
print(f"Numero di archi: {model.get_numArchi()} ")
model.buildGraph()
print(f"Numero di nodi: ", (model.get_numNodi()))
print(f"Numero di archi: {model.get_numArchi()} ")