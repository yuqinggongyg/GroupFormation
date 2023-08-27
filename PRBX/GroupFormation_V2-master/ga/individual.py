from .utils import *
import numpy as np
import random as rnd
import sys

# class that creates individual which contains genes 
class Individual:
    def __init__(self, id_to_characts, group_num):
        self.id_to_characts = id_to_characts
        self.student_num = len(id_to_characts)
        self.group_num = group_num
        self.group_size = self.student_num // group_num

    def init_random_genes(self):
        arr = np.array(list(self.id_to_characts.keys()))
        rng = np.random.default_rng()
        rng.shuffle(arr)
        self.genes = np.reshape(arr, (self.group_num, self.group_size))

        return self.init_fitness()

    def init_fitness(self):
        total_mean = calculate_total_mean(self.id_to_characts)
        individual_mean = calculate_individual_mean(self.id_to_characts, self.genes)
        square_difference = calculate_square_difference(total_mean, individual_mean)

        if square_difference == 0:
            self.fitness = sys.maxsize
        else:
            self.fitness = 1.0 / square_difference

        return self

    def crossover(self, partner):
        child = Individual(self.id_to_characts, self.group_num)
        child_genes = np.copy(self.genes)

        crossover_points = [rnd.randint(0, self.group_size) for _ in range(self.group_num)]
        genes_to_crossover = set()

        for point, group in zip(crossover_points, child_genes):
            for idx in range(point, self.group_size):
                genes_to_crossover.add(group[idx])

        genes_in_partner_order = [gene for group in partner.genes for gene in group if gene in genes_to_crossover]

        num = 0
        for point, group in zip(crossover_points, child_genes):
            for idx in range(point, self.group_size):
                group[idx] = genes_in_partner_order[num]
                num += 1

        child.genes = child_genes

        return child.init_fitness()


    def mutate(self, individual_mutate_rate, gene_mutate_rate):
        if rnd.uniform(0, 1) > individual_mutate_rate:
            return self
        for i in range(self.group_num):
            for j in range(self.group_size):
                if rnd.uniform(0, 1) > gene_mutate_rate:
                    continue

                # randomly select a value which is not the same row
                rnd_num = rnd.randrange(0, self.student_num)
                while rnd_num // self.group_size == i:
                    rnd_num = rnd.randrange(0, self.student_num)

                row = rnd_num // self.group_size
                col = rnd_num % self.group_size

                self.genes[i][j], self.genes[row][col] = self.genes[row][col], self.genes[i][j]

        return self.init_fitness()

