import numpy as np
import dimod

num_nodos = 6
num_colores = 3

num_variables = num_nodos * num_colores
P = 4#(num_colores - 1)**2
Q = 2

constante = num_nodos * P

adyacencias = [(0,1),(0,4),(1,2),(1,4),(1,3),(2,3),(3,4)]
J = {}
matriz = np.zeros((num_variables, num_variables), np.int8)

for i in range(0,num_nodos):
    for j in range(0,num_colores):
        fila = i*num_colores + j
        for k in range(0,num_colores):
            col = i*num_colores + k
            #if fila < col:
            matriz[fila][col] = P
            J[(fila,col)] = P
        print("i=",i,"num_nodos",num_nodos,"j",j)
        #if fila < col:
        matriz[i*num_colores + j][i*num_colores + j] = -P
        J[(i*num_colores + j,i*num_colores + j)] = -P
    
print(matriz)

for ad in adyacencias:
    print(ad, ad[0], ad[1])
    for i in range(0, num_colores):
        fila = ad[0] * num_colores + i
        col = ad[1] * num_colores + i
        print(ad, str(fila), ", ", str(col))
        #if fila < col:
        matriz[fila][col] = Q
        J[(fila,col)] = Q
        #else:
        matriz[col][fila] = Q
        J[(col,fila)] = Q

print(matriz)


# Veamos ahora un caso un poco más complicado
#J = {(0,1):1,(0,2):1,(1,2):1}

h = {}
print(J)
model = dimod.BinaryQuadraticModel(h, J, constante, dimod.BINARY) # QUBO
#model = modelQ.change_vartype(dimod.SPIN, inplace=False)
print("El modelo que vamos a resolver es")
print(model)
print()


# Primero lo resolvemos de forma exacta
from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(model)
print("La solucion exacta es")
#print(solution)
print()

# Ahora, con *simulated annealing*
sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=10)
print("La solucion con simulated annealing es")
print(response)
print()

# Finalmente, lo resolvemos nuevamente con el *quantum annealer*

#from dwave.system.samplers import DWaveSampler
#from dwave.system.composites import EmbeddingComposite
#sampler = EmbeddingComposite(DWaveSampler())
#response = sampler.sample(model, num_reads=5000)
#print("La solucion con el quantum annealer de D-Wave es")
#print(response)
#print()


