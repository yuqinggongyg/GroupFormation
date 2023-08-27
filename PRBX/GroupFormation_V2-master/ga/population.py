from .individual import *
import random as rnd
import bisect

# class that creates population and a pattern of individuals
class Population:
    def __init__(self, id_to_characts, group_num, population_size):
        self.id_to_characts = id_to_characts
        self.group_num = group_num
        self.population_size = population_size
        self.generation_num = 0

    def create_initial_population(self):
        self.individuals = []
        for _ in range(self.population_size):
            individual = Individual(self.id_to_characts, self.group_num)
            individual = individual.init_random_genes()
            self.individuals.append(individual)

        return self.init_fitnesses()

    def init_fitnesses(self):
        self.fitnesses = [individual.fitness for individual in self.individuals]
        self.accumlative_fitnesses = [self.fitnesses[0]]
        for i in range(1, len(self.fitnesses)):
            self.accumlative_fitnesses.append(self.accumlative_fitnesses[-1] + self.fitnesses[i])

        return self

    def roulette_wheel_select(self):
        random_point = rnd.uniform(0, self.accumlative_fitnesses[-1])
        idx = bisect.bisect_left(self.accumlative_fitnesses, random_point)

        return self.individuals[idx]

    def breed_next_generation(self, crossover_rate, individual_mutate_rate, gene_mutate_rate):
        self.generation_num += 1
        next_individuals = []
        crossover_chid_num = int(crossover_rate * self.population_size)
        keep_chid_num = self.population_size - crossover_chid_num

        for _ in range(keep_chid_num):
            next_individuals.append(self.roulette_wheel_select())

        for _ in range(crossover_chid_num):
            parent_A = self.roulette_wheel_select()
            parent_B = self.roulette_wheel_select()
            child = parent_A.crossover(parent_B)
            next_individuals.append(child)

        for i in range(self.population_size):
            next_individuals[i] = next_individuals[i].mutate(individual_mutate_rate, gene_mutate_rate)

        self.individuals = next_individuals

        return self.init_fitnesses()

    def get_fittest_individual(self):
        fittest_individual = self.individuals[0]

        for individual in self.individuals:
            if individual.fitness > fittest_individual.fitness:
                fittest_individual = individual

        return fittest_individual

    def get_population_avg_fitness(self):
        return sum(self.fitnesses) / self.population_size

