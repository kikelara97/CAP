import numpy as np
import dimod
import sys

# Se direcciona la salida de la ejecución al fichero "output.txt"
# Los print escribiran en ese fichero
sys.stdout = open("output.txt", "w")

print("Problema de coloreado de un grafo")

# En esta sección se podrán modificar los datos del problema a resolver
num_nodos = 6 # Número de nodos que componen el grafo
num_colores = 3 # Número máximo de colores a utilizar

print("  * El grafo tiene", num_nodos, "nodos")
print("  * Se pueden utilizar", num_colores, "colores")

# Las adyacencias se representan como una lista de pares (i,j) 
# Cada par representa que el nodo i y el j están conectados. 
# Al ser un grafo no dirigido solo hace falta incluir uno de los sentidos
# Debería haber tantos pares en la lista como arcos en el grafo
adyacencias = [(0,1),(0,5),(1,3),(2,3),(2,4),(2,5),(3,4),(4,5)]

# El incremento 1 con adyacencia también entre los nodos 1-2
#adyacencias.append((1,2))

# El incremento 2 con adyacencia entre los nodos 0-2
#adyacencias.append((0,2))

print("  * Se han indicado", len(adyacencias), "arcos en el grafo\n")

# Se obtienen los valores de penalización a aplicar según las restricciones
P = num_nodos - 1 # Un nodo solo puede tener un color
Q = num_colores - 1 # Los nodos adyacentes no pueden tener el mismo color

# El problema resuelto obtendra una energía de num_nodos * penalizacion P
offset = num_nodos * P # Se asigna el valor de offset a utilizar en BQM

# Inicialización de la matriz Q con valores 0.
# Al utilizar la notación dispersa solamente se incluirán los valores que no son 0
J = {}

# Se incluyen las penalizaciones para la restricción de que cada nodo solo
#  puede tener un colo
for i in range(0,num_nodos): # Se recorren todos los nodos
    for j in range(0,num_colores): # Se recorren los colores
        fila = i*num_colores + j # Fila cuyo valor hay que actualizar
        for k in range(0,num_colores): # Se recorren nuevamente los colores
            col = i*num_colores + k # Columna que se debe actualizar

            # Se fija la penalización positiva para todos los elementos 
            #  asignados a cada no
            J[(fila,col)] = P
            
        # Se fija la penalización negatica para los valores de la diagonal
        # Representaran la asignación de un nodo a un único color
        J[(fila,fila)] = -P
    
# Se incluyen tambien las penalizaciones por no cumplir la restricción
#  de que cada nodo debe tener un color diferentes al de sus adyacentes
for ad in adyacencias: # Se recorre cada una de las adyacencias indicadas
    for i in range(0, num_colores): # Se recorre cada uno de los colores
        fila = ad[0] * num_colores + i # Fila a actualizar (nodo i)
        col = ad[1] * num_colores + i # Columna a actualizar (nodo j)
        
        # Se penaliza que el nodo i y j tenga el mismo color
        J[(fila,col)] = Q
        J[(col,fila)] = Q # Garantiza la simetría de la matriz Q

# El valor de h indica el bias asociado al uso de cada una de las variables que 
#  componen el problema.
# En esta caso, todas las variables pueden ser utilizadas diferentemente
# En esta variable se podría indicar restricciones del estilo: "que se utilice lo
#  menos posible el color #2"
h = {}

# Definimos el modelo que repreentara nuestro problema como un modelo binario
#  cuadrático (BQM)
# Esta representación se corresponde con la notación de un modelo QUBO
model = dimod.BinaryQuadraticModel(h, J, offset, dimod.BINARY)

# Transformación a un problema del modelo de Ising 
model.change_vartype(dimod.SPIN)

print("El modelo que vamos a resolver es")
print(model)
print()

# Se resuelve el problema de forma exacta
from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(model)
print("La solucion exacta es")
print(solution)
print()

# Ahora se resuelve con simulated annealing
sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=20)
print("La solucion con simulated annealing es")
print(response)
print()

# Finalmente, lo resolvemos nuevamente con el *quantum annealer*
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(model, num_reads=5000)
print("La solucion con el quantum annealer de D-Wave es")
print(response)
print()

# Se cierra el flujo de la salida estándar
# Previene errores con el fichero
sys.stdout.close()
