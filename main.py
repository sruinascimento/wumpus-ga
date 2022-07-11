from ambiente import Ambiente
from individuo import Individuo

'''
    os Parâmetros   
'''


ag = Ambiente()
ag.inicializa()
print(ag.matriz_ambiente)
print('Melhor fitness por geracao', ag.melhorFitnessPorGeracao())
array = ag.melhorFitnessPorGeracao()
ag.graficoMelhorFitness(array)