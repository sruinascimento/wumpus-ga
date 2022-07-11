from ambiente import Ambiente
from individuo import Individuo

ag = Ambiente(4)
ag.inicializa()
print(ag.matriz_ambiente)
print('Melhor fitness por geracao', ag.melhorFitnessPorGeracao())
array = ag.melhorFitnessPorGeracao()
ag.graficoMelhorFitness(array)