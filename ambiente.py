from individuo import Individuo
import numpy as np
from random import sample, randint
import matplotlib.pyplot as plt


class Ambiente:

    def __init__(self, dimensao_quadrada: int = 4, tamanho_da_populacao:int = 20, geracao_de_parada:int = 10):  
        '''
            @params
            dimensao_quadrada : dimensão da matriz do ambiente
            ouro: número 10 para representar o ouro
            wumpus: número 5 para representar o wumpus
            poco: número 2 para representar o poço
            sensacoes: dicionário com as coordenadas das senções de brisa, brilho, fedor, morte pelo wumpus, morte pelo poço
            matriz_ambiente: matriz ambiente preenchida com os valores referente ao agente, poços, wumpus e o ouro
            tamanho_da_populacao: número referente ao total de indivíduos
            populacao: um lista de individuos(agentes) que representam a geração 0
            melhor_individuo: representa a melhor solução encontrada dentre todas gerações
            recombinacao_de_cromossomo: representa o percentual que usaremos para seleção e reprodução dos indivíduos
            taxa_de_mutacao: percentual para que haja variabilização genética
            geracao_de_parada: quantas gerações haverá para nosso AG
            todos_fitness: é um lista com todos os fitness de todas gerações
        '''
        self.dimensao_quadrada = dimensao_quadrada
        self.ouro:int = 10
        self.wumpus:int = 5
        self.poco:int = 2
        self.sensacoes =  {'brisa':  [], 'fedor':  [], 'brilho': [], 'morte_poco': [], 'morte_wumpus': []}
        self.matriz_ambiente: int = self.geraMatrizAmbiente(self.dimensao_quadrada)
        self.tamanho_da_populacao = tamanho_da_populacao
        self.populacao = self.geraPopulacao()
        self.melhor_individuo = None
        self.recombinacao_de_cromossomo = 0.9
        self.taxa_de_mutacao = 0.02
        self.geracao_de_parada = geracao_de_parada
        self.todos_fitness = []
       
    def inicializa(self):
        '''
            Principal método, esse método que é invocado para poder iniciar todo o processo.
            Primeira etapa será chamar a função movimentaPopulacao(), isso acarretará em dar passos aleatórios com as possibilidade
            N(norte), S(sul), L(leste) e O(oeste). A partir disso será invocado o método calculaFitnessPopulacao() para 
            avaliar os individuos da primeira geração.
            Posteriormente teremos um laço para iterar de acordo com a quantidade de gerações configuradas.
            Sempre realizando o processo de reprodução e avaliação da população.
            Ao final do processo, será apresentado a melhor solução encontrada.
        '''
        self.movimentaPopulacao()
        self.calculaFitnessPopulacao(self.populacao)

        for i in range(self.geracao_de_parada):
            nova_populacao = self.reproduz(self.populacao)
            self.calculaFitnessPopulacao(nova_populacao)

        print('Melhor Individuo ', self.melhor_individuo)

    def geraMatrizAmbiente(self, dimensaoQuadrada: int) -> np.ndarray:
        '''
            A função geraMatrizAmbiente() gera as coordenadas do Agente representado pelo número 1, 
            poços representados pelo número 2, wumpus representado pelo número 5, e por fim, o ouro representado
            pelo número 10.
            As regras são:
             Ambiente 4X4
             Poços: 3
             Ouro: 1
             Wumpus: 1
            
            Somente o agente pode estar na posição 0x0.
            O Wumpus não pode estar dentro de uma coordenada que tenha um poço.
            O Wumpus pode estar na coordenada do ouro.
        '''
        agente = 1
        ambiente = np.zeros(shape=(dimensaoQuadrada, dimensaoQuadrada))
        ambiente[0][0] = agente
        ambiente = self.geraCoordenadaPoco(ambiente)
        ambiente = self.geraCoordenadaOuro(ambiente)
        ambiente = self.geraCoordenadaWumpus(ambiente)

        self.geraCoordenadaSensacoes(ambiente)

        return ambiente

    def geraCoordenadaPoco(self, matriz_ambiente):
        '''
            Função que gera as coordenadas do poço
        '''
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
        '''
            Função que gera as coordenadas do ouro
        '''
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
        '''
            Função que gera a coordenada do wumpus
        '''
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
        '''
            Inicializa a geração 0 com instancia dos individuos, nossos agentes.
        '''
        populacao = [Individuo() for i in range(self.tamanho_da_populacao)]
        return populacao

    def movimentaPopulacao(self) -> None:
        '''
            Etapa para realizar a movimentação da populção 0.
        '''
        for _ in range(19):
            for agente in self.populacao:
                self.movimentaAgente(agente)

    def movimentaAgente(self, agente: Individuo) -> None:
        '''
            Função que realiza movimentos aleatórios sorteando N, S L e O.
        '''
        listaMovimentos = ['N', 'S', 'L', 'O']
        movimentoAleatorio = np.random.choice(listaMovimentos)
        coordenada_atual = agente.cromossomo[-1]
        coordenada_atualizada = self.atualizaCoordenadaDoAgente(
            movimentoAleatorio, coordenada_atual)
        agente.cromossomo.append(coordenada_atualizada)

    def atualizaCoordenadaDoAgente(self, movimento: str, coordenada_atual) -> list:

        '''
            Regras:
            Se a posição N(norte) for sorteada, a coordenada x, que representa a linha
            será decrementada de 1 unidade.
            
            Se a posição S(sul) for sorteada, a coordenada x, que representa a linha será
            incrementada em 1 unidade

            Se a posição L(leste) for sorteada, a coordenada y, que representa a coluna será
            incrementada em 1 unidade

            Se a posição O(Oeste) for sorteada, a coordenada y, que representa a coluna será
            decrementada em 1 unidade

        '''

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
        
        '''
            Função que gera um dicionário com todas as coordenadas com as senções de brisa, 
            odor e brilho. Ou seja, são as coordenadas adjacentes que contém as informações de sensações
        '''


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

        '''
            Função que valida as sensações somente em coordenadas dentro tabuleiro.
        '''

        coordenadas_com_sensacao = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        coordenadas_validas_sensacaoes = []
        for coordenada in coordenadas_com_sensacao:
            coordenada_valida = self.verificaCoordenadaValida(coordenada[0], coordenada[1],self.dimensao_quadrada )
            if coordenada_valida:
                coordenadas_validas_sensacaoes.append([coordenada[0], coordenada[1]])
        
        return coordenadas_validas_sensacaoes

    def calculaFitnessPopulacao(self, populacao: list) -> None:
        '''
            Função que itera todos agentes da população para calcular o fitness de cada.
        '''
        todos_fitness_populacao = []
        for agente in populacao:
            self.calculaFitnessDoAgente(agente)
            todos_fitness_populacao.append(agente.fitness)

        self.todos_fitness.append(todos_fitness_populacao)

    def calculaFitnessDoAgente(self, agente: Individuo) -> None:
        '''
           Cálculo do fitness com base nos nossos critérios:
           Valores: 
           -200 é a penalidade no fitness para o agente que caiu no poço
           -500 é a penalidade no fitness para o agente que morreu para o wumpus

           Há outros valores para penalidade dentro das funções.

           A função fitness é dividida em etapas.
           A primeira etapa é verificar se o agente pegou o ouro sem morrer.
           Caso seja verdade, o fitnesse receberá 1000 pontos por atingir o objetivo.
           Posteriormente, será verificado se ele andou dentro ou fora do tabuleiro. Por fim,
           O agente será avaliado se ele teleportou no mapa, ou seja, deu um passo maior do que 
           uma coordenada. Caso o individuo teleportou, ele será penalizado.
        '''
        valor_fitness = 0
        penalizacao_poco = -200
        penalizacao_wumpus = -500
        personagem_vivo = self.verificaPersonagemVivoAteOuro(agente)
        if personagem_vivo:
            valor_fitness += self.premiaPorPegarOuroVivo(personagem_vivo)
            valor_fitness += self.premiaPorAndarNoTabuleiro(agente.passo_ate_ouro)  
            valor_fitness += self.penalizaPorTeleportar(agente.cromossomo)
            agente.ouro = True
        else:
            valor_fitness += self.premiaPorAndarNoTabuleiro(agente.cromossomo) 
            valor_fitness += self.penalizaPorTeleportar(agente.cromossomo)
            valor_fitness += self.penalizaPorMorteDoAgente(agente.cromossomo, penalizacao_poco, 'morte_poco')
            valor_fitness += self.penalizaPorMorteDoAgente(agente.cromossomo, penalizacao_wumpus, 'morte_wumpus')
            
        agente.fitness = valor_fitness

        self.verificaMelhorIndividuo(agente)

    def melhorFitnessPorGeracao(self):
        '''
            Função que armazena os três melhores fitness de cada geração.
        '''
        melhores_fitness_ordenados = [sorted(fitness, reverse=True) for fitness in self.todos_fitness]
        melhores_fitness_ordenados = [[fitness[0], fitness[1], fitness[2]] for fitness in melhores_fitness_ordenados]
        return melhores_fitness_ordenados

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

    def verificaPersonagemVivoAteOuro(self, agente:Individuo) -> bool:
        '''
            Função que retorna um valor booleano, caso a agente não tenha morrido até encontrar 
            o ouro.
        '''

        coordenada_ouro = self.sensacoes['brilho'][0]
        try:
            indice_ouro = agente.cromossomo.index(coordenada_ouro)
        except:
            indice_ouro = -1

        if indice_ouro == -1:
            return False
        coordenadas_morte = self.sensacoes['morte_poco'] + self.sensacoes['morte_wumpus']
     
        for poco_e_wumpus in coordenadas_morte:
            passo_antes_do_ouro = agente.cromossomo[0:indice_ouro]
            if poco_e_wumpus in passo_antes_do_ouro:
                return False
        
        agente.passo_ate_ouro = agente.cromossomo[0:indice_ouro+1]
        return True

    def premiaPorPegarOuroVivo(self, personagem_vivo:bool):
        premiacao_ouro = 1000
        fitness = 0
        if not personagem_vivo:
            return fitness
        fitness = premiacao_ouro
        return fitness

    def verificaCoordenadaValida(self, x, y, dimensao) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= dimensao or y >= dimensao:
            return False
        
        return True

    def verificaMelhorIndividuo(self, agente: Individuo) -> None:
        '''
            Verifica qual é a melhor solução de todas
        '''
        if not self.melhor_individuo:
            self.melhor_individuo = agente
            return

        if self.melhor_individuo.fitness < agente.fitness:
            self.melhor_individuo = agente.copia()
            return

    def selecionaIndividuos(self, populacao: list) -> list:
        '''
            Seleção de indivíduos pelo método torneio.
            É seleciondo 90% da população. Serão escolhidos 3 agentes, ordenados e sempre será 
            escolhido o agente pelo melhor fitness
        '''
        total_selecionados = self.totalSelecionados()
        piscina = []
        for _ in range(total_selecionados):
            selecionados = sample(populacao, 3)
            selecionados.sort(key=lambda individuo: individuo.fitness, reverse=True)
            piscina.append(selecionados[0])

        return piscina

    def totalSelecionados(self) -> int:
        '''
            Retorna um valor inteiro que será usado para seleção, reprodução e mutação.
        '''
        return int(self.tamanho_da_populacao * self.recombinacao_de_cromossomo)

    def reproduzIndividuos(self, populacao_selecionada: list) -> list:
        '''
            Método de repodução seleciona um pai e uma mãe ao acaso. E a cadas dois pais selecionados,
            serão gerados dois novos filhos
        '''
        total_selecionados = self.totalSelecionados()
        novos_filhos = []
        for _ in range(total_selecionados):
            pai, mae = sample(populacao_selecionada, 2)
            filhos = self.geraFilho(pai, mae)
            novos_filhos.extend(filhos)

        return novos_filhos

    def geraFilho(self, pai, mae) -> tuple:
        '''
            Reprodução com 1 ponto de corte. Um ponto será sorteado. E esse será o ponto para gera 
            dois filhos
        '''
        tamanho_cromossomo = len(pai.cromossomo)
        ponto_corte = np.random.randint(1, tamanho_cromossomo)
        primeiro_filho = pai.cromossomo[0:ponto_corte] + mae.cromossomo[ponto_corte:]
        segundo_filho = mae.cromossomo[0:ponto_corte] + pai.cromossomo[ponto_corte:]

        return (Individuo(primeiro_filho), Individuo(segundo_filho))

    def mutaIndividuo(self, populacao: list) -> None:
        '''
        Mutando os agentes, para que haja a variabilidade genética. O percentual de mutação
        varia entre 2% e 5%, para que um individuo não se modifique muito.
        '''
        for agente in populacao:
            mutacao_atingida = np.random.random() <= self.taxa_de_mutacao
            if mutacao_atingida:
                self.muta(agente)

    def muta(self, agente: Individuo) -> None:
        '''
            A mutação para as coordenadas, deverá sortear um número aleatório para verificar se 
            a coordenada x ou y será modificada. E por fim será sorteado outro número aleatório, para
            definir se a coordenada x ou y, será incrementada ou decrementada.
        '''
       
        tamanho_cromossomo = len(agente.cromossomo)
        posicao_sorteada = np.random.randint(0, tamanho_cromossomo)
        incremento = np.random.random()
        posicao_x = np.random.random() <= 0.5
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
        Processo completo de reprodução:
        1º ordenação dos individuos
        2º seleção de individuos
        3º reprodução dos individuos a partir dos agentes selecionados
        4º mutação dos individuos
        5º nova geração contem 10% da população anterior.
        '''
        populacao.sort(key=lambda agente: agente.fitness)
        total_selecionados = self.totalSelecionados()
        individuos_selecionados = self.selecionaIndividuos(populacao)
        nova_populacao = self.reproduzIndividuos(individuos_selecionados)
        self.mutaIndividuo(nova_populacao)
        populacao_nova_geracao = nova_populacao + populacao[total_selecionados:]

        return populacao_nova_geracao
    
    def graficoMelhorFitness(self, array,x=16,y=7):
        '''
        Função responsavel por gerar o gráfico dos 3 melhores fitness de
        de cada geração.
        Args:
        array: (ndarray) array com os 3 melhores fitness por geração.
        x, y: dimensões para criação do gráfico.
        '''   
        array = np.array(array)
        plt.figure(figsize=(x,y))
        x = np.arange(array.shape[0]) 
        width = 0.30
        y = np.arange(0,1080,40)
        plt.bar(x, array[:,0], width) 
        plt.bar(x+0.3, array[:,1], width)
        plt.bar(x+0.6, array[:,2], width)
        plt.xticks(x+0.3, ['Geração 0', 'Geração 1', 'Geração 2', 'Geração 3', 'Geração 4', 'Geração 5', 'Geração 6', 'Geração 7', 'Geração 8', 'Geração 9', 'Geração 10']) 
        plt.yticks(y)
        plt.ylabel("Valor do Fitness") 
        plt.title('OS TRÊS MELHORES FITNESS DE ONZE GERAÇÕES', fontsize=14, weight='bold')
        plt.legend(["1º Lugar", "2º Lugar", "3º Lugar"], title='Top 3 Fitness')
        plt.grid()
        plt.show()