class Individuo:

    def __init__(self):
        self.fitness = 0
        self.cromossomo = [ [0, 0] ]

    def __repr__(self):
        return f'cromossomo: {self.cromossomo}\nfitness {self.fitness}\n'