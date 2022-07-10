from individuo import Individuo
import numpy as np
from random import sample, randint


class Ambiente:

    def __init__(self, dimensao_quadrada: int):
        self.dimensao_quadrada = dimensao_quadrada
        self.ouro:int = 10
        self.wumpus:int = 5
        self.poco:int = 2
        self.matriz_ambiente: int = self.geraMatrizAmbiente(self.dimensao_quadrada)
        self.tamanho_da_populacao = 10
        self.populacao = self.geraPopulacao()
        self.melhor_individuo = None
        self.recombinacao_de_cromossomo = 0.9
        self.taxa_de_mutacao = 0.02
        self.geracao_de_parada = 2
        self.sensacoes = self.geraCoordenadaSensacoes()
       
    def inicializa(self):
        self.movimentaPopulacao()
        self.calculaFitnessPopulacao(self.populacao)
        print('Populacao 0')
        print(self.populacao)
        for i in range(self.geracao_de_parada):
            print(f'Geração {i + 1}')
            nova_populacao = self.reproduz(self.populacao)
            self.calculaFitnessPopulacao(nova_populacao)
            print(nova_populacao)

            print('\n\n\nMUDOU A GERACAO')
            print(self.melhor_individuo)

    def geraMatrizAmbiente(self, dimensaoQuadrada: int) -> np.ndarray:
        agente = 1
        ambiente = np.zeros(shape=(dimensaoQuadrada, dimensaoQuadrada))
        ambiente[0][0] = agente
        ambiente = self.geraCoordenadaPoco(ambiente)
        ambiente = self.geraCoordenadaOuro(ambiente)
        ambiente = self.geraCoordenadaWumpus(ambiente)

        return ambiente

    def geraCoordenadaPoco(self, matriz_ambiente):
        lista_coordenadas = []
        while (len(lista_coordenadas) < self.dimensao_quadrada - 1):
            coordenada_x, coordenada_y = randint(0, 3), randint(0, 3)
            if (coordenada_x == 0 and coordenada_y == 0):
                continue
            if ([coordenada_x, coordenada_y] not in lista_coordenadas):
                lista_coordenadas.append([coordenada_x, coordenada_y])
        for coordenada in lista_coordenadas:
            x, y = coordenada
            matriz_ambiente[x][y] = self.poco
        
        return matriz_ambiente

    def geraCoordenadaOuro(self, matriz_ambiente):
        while (True):
            coordenada_x, coordenada_y = randint(0, 3), randint(0, 3)
            if coordenada_x == 0 and coordenada_y == 0:
                continue
            if matriz_ambiente[coordenada_x][coordenada_y] == self.poco:
                continue
            
            matriz_ambiente[coordenada_x][coordenada_y] = self.ouro
            break
        return matriz_ambiente
    
    def geraCoordenadaWumpus(self, matriz_ambiente):
        while (True):
            coordenada_x, coordenada_y = randint(0, 3), randint(0, 3)
            if coordenada_x == 0 and coordenada_y == 0:
                continue
            if matriz_ambiente[coordenada_x][coordenada_y] == self.poco:
                continue

            if matriz_ambiente[coordenada_x][coordenada_y] == self.ouro:
                matriz_ambiente[coordenada_x][coordenada_y]+= self.wumpus
                break
            
            matriz_ambiente[coordenada_x][coordenada_y] = self.wumpus
            break
        return matriz_ambiente

    def geraPopulacao(self) -> list:
        populacao = [Individuo() for i in range(self.tamanho_da_populacao)]
        return populacao

    def movimentaPopulacao(self) -> None:
        for _ in range(19):
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

        if (movimento == NORTE):
            x -= 1

        if (movimento == SUL):
            x += 1

        if (movimento == LESTE):
            y += 1

        if (movimento == OESTE):
            y -= 1

        return [x, y]

    def geraCoordenadaSensacoes(self):
        sensacoes = {'brisa':  [], 'fedor':  [], 'brilho': []}
        
        for x in range(self.dimensao_quadrada):
            for y in range(self.dimensao_quadrada):
        
                if self.matriz_ambiente[x][y] == 2:
                    coordenadas = self.validaCoordenadasDasSensacoes(x, y)
                    sensacoes['brisa'].extend(coordenadas)
                
                if self.matriz_ambiente[x][y] == 5:
                    coordenadas = self.validaCoordenadasDasSensacoes(x, y)   
                    sensacoes['fedor'].extend(coordenadas)

                if self.matriz_ambiente[x][y] == 10:
                    sensacoes['brilho'].append([x, y])
        
        return sensacoes

    def validaCoordenadasDasSensacoes(self, x, y):
        coordenadas_com_sensacao = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        coordenadas_validas_sensacaoes = []
        for coordenada in coordenadas_com_sensacao:
            coordenada_valida = self.verificaCoordenadaValida(coordenada[0], coordenada[1],self.dimensao_quadrada )
            if coordenada_valida:
                coordenadas_validas_sensacaoes.append([coordenada[0], coordenada[1]])
        
        return coordenadas_validas_sensacaoes

    def calculaFitnessPopulacao(self, populacao: list) -> None:
        for agente in populacao:
            self.avaliaOAgente(agente)

    def avaliaOAgente(self, agente: Individuo) -> None:
        '''
            Alem de avaliar se o agente andou fora do tabuleiro, é necessário avaliar os passos
            válidos. Se ele deu um passo por cada vez, e não se "teleportou".
        '''
        punicao_fora_tabuleiro = -2
        punicao_teleporte = -1000
        premiacao = 1
        valor_fitness = 0
        for coordenadas in agente.cromossomo:
            x, y = coordenadas
            coordenada_valida = self.verificaCoordenadaValida(x, y, self.dimensao_quadrada)
            if coordenada_valida:
                valor_fitness += premiacao
            else:
                valor_fitness += punicao_fora_tabuleiro
            # if x < 0 or y < 0:
            #     valor_fitness += punicao_fora_tabuleiro
            # elif x >= self.dimensao_quadrada or y >= self.dimensao_quadrada:
            #     valor_fitness += punicao_fora_tabuleiro
            # else:
            #     valor_fitness += premiacao

        for i in range(len(agente.cromossomo) - 1):
            x, y = agente.cromossomo[i]
            coordenadas_validas = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
            proxima_coordenada = agente.cromossomo[i + 1]
            if proxima_coordenada not in coordenadas_validas:
                valor_fitness += punicao_teleporte

        agente.fitness = valor_fitness

        self.verificaMelhorIndividuo(agente)

    def verificaCoordenadaValida(self, x, y, dimensao) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= dimensao or y >= dimensao:
            return False
        
        return True

    def verificaMelhorIndividuo(self, agente: Individuo) -> None:
        if not self.melhor_individuo:
            self.melhor_individuo = agente
            return

        if self.melhor_individuo.fitness < agente.fitness:
            self.melhor_individuo = agente.copia()
            return

    def selecionaIndividuos(self, populacao: list) -> list:
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

    def reproduzIndividuos(self, populacao_selecionada: list) -> list:
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
        # print('Ponto de corte', ponto_corte)
        # print('PAI', pai)
        # print('MAE', mae)
        primeiro_filho = pai.cromossomo[0:ponto_corte] + mae.cromossomo[ponto_corte:]
        segundo_filho = mae.cromossomo[0:ponto_corte] + pai.cromossomo[ponto_corte:]
        # print('1f', primeiro_filho)
        # print('2f', segundo_filho)

        return (Individuo(primeiro_filho), Individuo(segundo_filho))

    def mutaIndividuo(self, populacao: list) -> None:
        '''
        Mutando os agentes
        '''
        for agente in populacao:
            mutacao_atingida = np.random.random() <= self.taxa_de_mutacao
            if mutacao_atingida:
                self.muta(agente)

    def muta(self, agente: Individuo) -> None:
        '''
        Bit string mutation
        '''
        # print('Agente antes de ser mutado')
        # print(agente)
        tamanho_cromossomo = len(agente.cromossomo)
        posicao_sorteada = np.random.randint(0, tamanho_cromossomo)
        incremento = np.random.random()
        posicao_x = np.random.random() <= 0.5
        # refatorar para uma função
        if posicao_x:
            if incremento > 0.5:
                agente.cromossomo[posicao_sorteada][0] += 1
            else:
                agente.cromossomo[posicao_sorteada][0] -= 1
        else:
            if incremento > 0.5:
                agente.cromossomo[posicao_sorteada][1] += 1
            else:
                agente.cromossomo[posicao_sorteada][1] -= 1

    def reproduz(self, populacao: list) -> list:
        '''
        realizar a reprodução completa
        '''
        populacao.sort(key=lambda agente: agente.fitness)
        total_selecionados = self.totalSelecionados()
        individuos_selecionados = self.selecionaIndividuos(populacao)
        nova_populacao = self.reproduzIndividuos(individuos_selecionados)
        self.mutaIndividuo(nova_populacao)
        populacao_nova_geracao = nova_populacao + populacao[total_selecionados:]

        return populacao_nova_geracao


