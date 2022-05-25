class Chromosome:
    def __init__(self, permutation, distance, roulette_prob, roulette_range_start, roulette_range_finish):
        self.permutation = permutation
        self.distance = distance
        self.roulette_prob = roulette_prob
        self.roulette_range_start = roulette_range_start
        self.roulette_range_finish = roulette_range_finish
