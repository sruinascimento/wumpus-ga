from audioop import reverse
from individuo import Individuo
import numpy as np
from random import sample

class Ambiente:

    def __init__(self, dimensaoQuadrada: int):
        self.matriz_ambiente: int = self.geraMatrizAmbiente(dimensaoQuadrada)
        self.tamanho_da_populacao = 20
        self.populacao = self.geraPopulacao()
        self.melhor_individuo = None
        self.recombinacao_de_cromossomo = 0.9

    def inicializa(self):
        self.movimentaPopulacao()
        self.calculaFitnessPopulacao(self.populacao)
        # print('Selecionados: ', self.selecionaIndividuos(self.populacao))
        print("POPULACAO")
        print(self.populacao)
        print('\nMELHOR')
        print(self.melhor_individuo)

    def geraMatrizAmbiente(self, dimensaoQuadrada: int) -> np.ndarray:
        agente = 1
        ambiente = np.zeros(shape=(dimensaoQuadrada, dimensaoQuadrada))
        ambiente[0][0] = agente
        return ambiente

    def geraPopulacao(self) -> list:
        populacao = [Individuo() for i in range(self.tamanho_da_populacao)]
        return populacao

    def movimentaPopulacao(self) -> None:
        for _ in range(32):
            for agente in self.populacao:
                self.movimentaAgente(agente)

    def movimentaAgente(self, agente: Individuo) -> None:
        listaMovimentos = ['N', 'S', 'L', 'O']
        movimentoAleatorio = np.random.choice(listaMovimentos)
        coordenada_atual = agente.cromossomo[-1]
        coordenada_atualizada = self.atualizaCoordenadaDoAgente(
            movimentoAleatorio, coordenada_atual)
        agente.cromossomo.append(coordenada_atualizada)

    def atualizaCoordenadaDoAgente(self, movimento: str, coordenada_atual) -> list:
        NORTE = 'N'
        SUL = 'S'
        LESTE = 'L'
        OESTE = 'O'
        x, y = coordenada_atual

        if(movimento == NORTE):
            x -= 1

        if(movimento == SUL):
            x += 1

        if(movimento == LESTE):
            y += 1

        if(movimento == OESTE):
            y -= 1

        return [x, y]

    def calculaFitnessPopulacao(self, populacao: list) -> None:
        for agente in populacao:
            self.avaliaOAgente(agente)

    def avaliaOAgente(self, agente: Individuo) -> None:
        valor_fitness = 0
        for coordenadas in agente.cromossomo:
            x, y = coordenadas
            if x < 0 or y < 0:
                valor_fitness -= 2
            else:
                valor_fitness += 1
        agente.fitness = valor_fitness
        self.verificaMelhorIndividuo(agente)
    
    def verificaMelhorIndividuo(self, agente:Individuo) -> None:
        if not self.melhor_individuo:
            self.melhor_individuo = agente
            return

        if self.melhor_individuo.fitness < agente.fitness:
            self.melhor_individuo = agente.copia()
            return        

    def selecionaIndividuos(self, populacao:list) ->list:
        total_selecionados = self.totalSelecionados()
        piscina = []
        for _ in range(total_selecionados):
            selecionados = sample(populacao, 3)
            selecionados.sort(key=lambda individuo: individuo.fitness, reverse=True)
            piscina.append(selecionados[0])		
	    
        return piscina

    def totalSelecionados(self) -> int:
        return int(self.tamanho_da_populacao * self.recombinacao_de_cromossomo)


    

            
