from individuo import Individuo
import numpy as np
from random import sample, randint


class Ambiente:

    def __init__(self, dimensao_quadrada: int):
        self.dimensao_quadrada = dimensao_quadrada
        self.ouro:int = 10
        self.wumpus:int = 5
        self.poco:int = 2
        self.sensacoes =  sensacoes = {'brisa':  [], 'fedor':  [], 'brilho': [], 'morte_poco': [], 'morte_wumpus': []}
        self.matriz_ambiente: int = self.geraMatrizAmbiente(self.dimensao_quadrada)
        self.tamanho_da_populacao = 20
        self.populacao = self.geraPopulacao()
        self.melhor_individuo = None
        self.recombinacao_de_cromossomo = 0.9
        self.taxa_de_mutacao = 0.02
        self.geracao_de_parada = 10
       
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

        self.geraCoordenadaSensacoes(ambiente)

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
            self.sensacoes['morte_poco'].append([x, y])
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
            self.sensacoes['morte_wumpus'].append([coordenada_x, coordenada_y])
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

    def geraCoordenadaSensacoes(self, matriz_ambiente:list) -> None:
        
        for x in range(self.dimensao_quadrada):
            for y in range(self.dimensao_quadrada):
        
                if matriz_ambiente[x][y] == 2:
                    coordenadas = self.validaCoordenadasDasSensacoes(x, y)
                    self.sensacoes['brisa'].extend(coordenadas)
                
                if matriz_ambiente[x][y] == 5:
                    coordenadas = self.validaCoordenadasDasSensacoes(x, y)   
                    self.sensacoes['fedor'].extend(coordenadas)

                if matriz_ambiente[x][y] == 10:
                    self.sensacoes['brilho'].append([x, y])

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
            self.calculaFitnessDoAgente(agente)

    def calculaFitnessDoAgente(self, agente: Individuo) -> None:
        '''
            Alem de avaliar se o agente andou fora do tabuleiro, é necessário avaliar os passos
            válidos. Se ele deu um passo por cada vez, e não se "teleportou".
        '''
        valor_fitness = 0
        penalizacao_poco = -200
        penalizacao_wumpus = -500
        valor_fitness += self.premiaPorAndarNoTabuleiro(agente.cromossomo)
        valor_fitness += self.penalizaPorTeleportar(agente.cromossomo)
        personagem_vivo = self.verificaPersonagemVivoAteOuro(agente.cromossomo)
        if personagem_vivo:
            valor_fitness += self.premiaPorPegarOuroVivo(personagem_vivo)
            agente.ouro = True

        # valor_fitness += self.penalizaPorMorteDoAgente(agente.cromossomo, penalizacao_poco, 'morte_poco')
        # valor_fitness += self.penalizaPorMorteDoAgente(agente.cromossomo, penalizacao_wumpus, 'morte_wumpus')
        agente.fitness = valor_fitness

        self.verificaMelhorIndividuo(agente)

    def premiaPorAndarNoTabuleiro(self, cromossomo:list) -> int:
        punicao_fora_tabuleiro = -2
        premiacao = 1
        fitness = 0
        for coordenadas in cromossomo:
            x, y = coordenadas
            coordenada_valida = self.verificaCoordenadaValida(x, y, self.dimensao_quadrada)
            if coordenada_valida:
                fitness += premiacao
            else:
                fitness += punicao_fora_tabuleiro

        return fitness

    def penalizaPorTeleportar(self, cromossomo:list) -> int:
        fitness = 0
        punicao_teleporte = -1000

        for i in range(len(cromossomo) - 1):
            x, y = cromossomo[i]
            coordenadas_validas = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
            proxima_coordenada = cromossomo[i + 1]
            if proxima_coordenada not in coordenadas_validas:
                fitness += punicao_teleporte

        return fitness

    def penalizaPorMorteDoAgente(self, cromossomo:list, penalizacao:int, chave_sensacao:str) -> int:
        penalizacao_morte = penalizacao
        fitness = 0
        coordenada_poco = self.sensacoes[chave_sensacao]
        for coordenada in coordenada_poco:
            if coordenada in cromossomo:
                fitness += penalizacao_morte
                break
        
        return fitness

    def verificaPersonagemVivoAteOuro(self, cromossomo:list) -> bool:
        coordenada_ouro = self.sensacoes['brilho'][0]
        try:
            indice_ouro = cromossomo.index(coordenada_ouro)
        except:
            indice_ouro = -1
        print('indice_ouro', indice_ouro)
        if indice_ouro == -1:
            return False
        
        for coordenada_poco in self.sensacoes['morte_poco']:
            print('coordenada_pocos>>>', coordenada_poco)
            passo_antes_do_ouro = cromossomo[0:indice_ouro]
            print('Passos antes do Ouro ', passo_antes_do_ouro)
            if coordenada_poco in passo_antes_do_ouro:
                return False
        
        return True

    def premiaPorPegarOuroVivo(self, personagem_vivo:bool):
        premiacao_ouro = 1000
        fitness = 0
        if not personagem_vivo:
            return fitness
        fitness = premiacao_ouro
        return fitness

    # def premiaPorPegarOuro(self, cromossomo:list) -> int:
    #     personagem_vivo = self.verificaPersonagemVivoAteOuro(cromossomo)
    #     fitness = 0
    #     fitness += self.premiaPorPegarOuroVivo(personagem_vivo)
        
    #     return fitness


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