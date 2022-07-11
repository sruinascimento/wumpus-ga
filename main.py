from ambiente import Ambiente
from individuo import Individuo

ag = Ambiente(4)
# ag.movimentaAgente()
# ag.movimentaAgente()
# ag.movimentaAgente()
# ag.movimentaAgente()
# print(ag.agente.cromossomo)
ag.inicializa()
print(ag.matriz_ambiente)
# print(ag.sensacoes)
print('Melhor fitness por geracao', ag.melhorFitnessPorGeracao())