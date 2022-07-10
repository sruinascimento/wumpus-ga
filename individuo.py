class Individuo:

    def __init__(self, cromossomo=None):
        self.fitness = 0
        self.cromossomo = [ [0, 0] ] if not cromossomo else cromossomo
        self.ouro = False

    def copia(self):
        individuo_temporario = Individuo(self.cromossomo)
        individuo_temporario.fitness = self.fitness
        return individuo_temporario

    def __repr__(self):
        return f'cromossomo: {self.cromossomo}\nfitness {self.fitness}\npegou ouro: {self.ouro}\n'