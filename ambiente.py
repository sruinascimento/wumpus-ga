from individuo import Individuo
import numpy as np
from random import sample

class Ambiente:

    def __init__(self, dimensaoQuadrada: int):
        self.matriz_ambiente: int = self.geraMatrizAmbiente(dimensaoQuadrada)
        self.tamanho_da_populacao = 10
        self.populacao = self.geraPopulacao()
        self.melhor_individuo = None
        self.recombinacao_de_cromossomo = 0.9
        self.taxa_de_mutacao = 0.02

    def inicializa(self):
        self.movimentaPopulacao()
        self.calculaFitnessPopulacao(self.populacao)
        print('POP 0')
        print(self.populacao)
        individuos_selecionados = self.selecionaIndividuos(self.populacao)
        nova_populacao = self.reproduzIndividuos(individuos_selecionados)
        # print('NOVA POPULACAO')
        # print(nova_populacao)
        # print('Selecionados: ', self.selecionaIndividuos(self.populacao))
        # print("POPULACAO")
        # print(self.populacao)
        # print('\nMELHOR')
        # print(self.melhor_individuo)

    def geraMatrizAmbiente(self, dimensaoQuadrada: int) -> np.ndarray:
        agente = 1
        ambiente = np.zeros(shape=(dimensaoQuadrada, dimensaoQuadrada))
        ambiente[0][0] = agente
        return ambiente

    def geraPopulacao(self) -> list:
        populacao = [Individuo() for i in range(self.tamanho_da_populacao)]
        return populacao

    def movimentaPopulacao(self) -> None:
        for _ in range(20):
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
        '''
            Alem de avaliar se o agente andou fora do tabuleiro, é necessário avaliar os passos 
            válidos. Se ele deu um passo por cada vez, e não se "teleportou".
        '''
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
        '''
        Seleção pelo método de Torneio
        '''
        total_selecionados = self.totalSelecionados()
        piscina = []
        for _ in range(total_selecionados):
            selecionados = sample(populacao, 3)
            selecionados.sort(key=lambda individuo: individuo.fitness, reverse=True)
            piscina.append(selecionados[0])		
	    
        return piscina

    def totalSelecionados(self) -> int:
        return int(self.tamanho_da_populacao * self.recombinacao_de_cromossomo)

    def reproduzIndividuos(self, populacao_selecionada:list) -> list:
        total_selecionados = self.totalSelecionados()
        novos_filhos = []
        for _ in range(total_selecionados):
            pai, mae = sample(populacao_selecionada, 2)
            filhos = self.geraFilho(pai, mae)
            novos_filhos.extend(filhos)
        
        return novos_filhos

    def geraFilho(self, pai, mae) -> tuple:
        '''
        Reprodução com 1 ponto de corte
        '''
        tamanho_cromossomo = len(pai.cromossomo)
        ponto_corte = np.random.randint(1, tamanho_cromossomo)
        print('Ponto de corte', ponto_corte)
        print('PAI', pai)
        print('MAE', mae)
        primeiro_filho = pai.cromossomo[0:ponto_corte] + mae.cromossomo[ponto_corte:]
        segundo_filho = mae.cromossomo[0:ponto_corte] + pai.cromossomo[ponto_corte:]
        print('1f', primeiro_filho)
        print('2f', segundo_filho)

        return (Individuo(primeiro_filho), Individuo(segundo_filho))
	
    def mutaIndividuo(self, populacao:list):
        '''
        Mutando os agentes
        '''
        for agente in populacao:
            mutacao_atingida = np.random.random() <= self.taxa_de_mutacao 
            if mutacao_atingida:
                self.muta(agente)

    def muta(self, agente:Individuo):
        '''
        Bit string mutation 
        '''
        print('Agente antes de ser mutado')
        print(agente)
        tamanho_cromossomo = len(agente.cromossomo)
        posicao_sorteada = np.random.randint(0, tamanho_cromossomo)
        incremento = np.random.random()
        posicao_x = np.random.random() <= 0.5
        #refatorar para uma função
        if posicao_x :
            if incremento > 0.5:
                agente.cromossomo[posicao_sorteada][0] += 1
            else:
                agente.cromossomo[posicao_sorteada][0] -= 1
        else:
            if incremento > 0.5:
                agente.cromossomo[posicao_sorteada][1] += 1
            else:
                agente.cromossomo[posicao_sorteada][1] -= 1

        print('Agente depois de ser mutado')
        print(agente)

    def reproducao(self):
        '''
        realizar a reprodução completa
        '''
        pass





# def main():
#     i1 = Individuo([[1, 2], [2, 2]])
#     ag = Ambiente(4)
#     ag.muta(i1)

# if __name__ == "__main__":
#     main()

            
