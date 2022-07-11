class Individuo:

    def __init__(self, cromossomo=None):
        self.fitness = 0
        self.cromossomo = [ [0, 0] ] if not cromossomo else cromossomo
        self.ouro = False
        self.passo_ate_ouro = []

    def copia(self):
        individuo_temporario = Individuo(self.cromossomo)
        individuo_temporario.fitness = self.fitness
        individuo_temporario.ouro = self.ouro
        individuo_temporario.passo_ate_ouro = self.passo_ate_ouro
        return individuo_temporario

    def __repr__(self):
        return f'cromossomo: {self.cromossomo}\nfitness {self.fitness}\npegou ouro: {self.ouro}\npassos até o ouro: {self.passo_ate_ouro}'