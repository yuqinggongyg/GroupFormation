from .individual import Individual
from .population import Population
from .config import *

def run(id_to_characts, group_num):
    population = Population(id_to_characts, group_num, POPULATION_SIZE).create_initial_population()

    global_fittest_score = -1
    global_fittest_individual = None

    while population.generation_num < MAX_GENERATION_NUM:
        print("generation number: ", population.generation_num);
        print("best individual score", population.get_fittest_individual().fitness)
        print("best individual:\n", population.get_fittest_individual().genes)
        print("generation average fitness", population.get_population_avg_fitness())
        print("#################################################################################")

        if (population.get_fittest_individual().fitness > global_fittest_score):
            global_fittest_score = population.get_fittest_individual().fitness
            global_fittest_individual = population.get_fittest_individual()

        population = population.breed_next_generation(CROSSOVER_RATE, INDIVIDUAL_MUTATE_RATE, GENE_MUTATE_RATE)

    answer = global_fittest_individual.genes
    print("final individual score", global_fittest_score)
    print("Final individual is:\n", answer)

    return answer
