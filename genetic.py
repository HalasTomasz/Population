import math

import random
import chromosome


def calc_dist(graph, permutation):
    dis = 0
    for i in range(0, len(permutation)):
        dis = dis + graph[permutation[i]][permutation[(i + 1) % len(permutation)]]['weight']
    return dis


# generujemy populację początkową (tutaj losowo, można potem wrzucić to w osobną funkcję i generować start przekazując
# funkcję w argumencie
# zwraca słownik: klucz - permutacja, wartość - wartość funkcji celu
def generate_start_population(graph, start_size):
    start_population = []
    i = 0
    while i < start_size:
        permutation = list(range(1, graph.number_of_nodes() + 1))
        random.shuffle(permutation)
        if permutation not in [x[0] for x in start_population]:
            start_population.append((permutation, calc_dist(graph, permutation)))
            i += 1

    return start_population


# selekcja rodziców, niektórzy się powtarzają, niektórzy mogą się nie powtórzyć
# ruletka
def selection(generation, population_size):
    # ewaluacja osobników
    distance_sum = sum([x[1] for x in generation])
    total_adaptation_points = 0
    for distance in [x[1] for x in generation]:
        total_adaptation_points += distance_sum / distance

    # ustawiamy prawdopodobieństwo każdego osobnika, tutaj mniejsza odległość - większe prawdopodobieństwo
    genotype = []
    roulette_compartment = 0.0
    for (permutation, distance) in [x for x in generation]:
        roulette_prob = (distance_sum / distance) / total_adaptation_points
        genotype.append(chromosome.Chromosome(
            permutation, distance, roulette_prob, roulette_compartment, roulette_compartment + roulette_prob))
        roulette_compartment += roulette_prob

    # selekcja
    children_parents = []
    for i in range(population_size):
        rand_1 = random.random()
        first_parent = get_parent(genotype, rand_1)
        rand_2 = random.random()
        second_parent = get_parent(genotype, rand_2)
        children_parents.append((first_parent, second_parent))
    return children_parents


# funkcja pomocnicza, wyciąga wylosowanego rodzica
def get_parent(genotype, random_number):
    for parent in genotype:
        if parent.roulette_range_start <= random_number <= parent.roulette_range_finish:
            return parent
    return None


# krzyżowanie osobników - tutaj użyty jest order crossover, dwupunktowy
def crossover(graph, selected_parents, i, j):
    new_generation = []

    # generujemy parę dzieci dla każdej pary rodziców
    for (first_parent, second_parent) in selected_parents:
        first_child = get_child(graph, first_parent, second_parent, i, j)
        second_child = get_child(graph, second_parent, first_parent, i, j)

        new_generation.append((first_child, calc_dist(graph, first_child)))
        new_generation.append((second_child, calc_dist(graph, second_child)))

    return new_generation


# pomocnicza funkcja do generowania dziecka
def get_child(graph, center_parent, border_parent, i, j):
    child = [None] * graph.number_of_nodes()
    used_numbers = []

    # środek dziecka jest środkiem jednego z rodziców
    for center_parent_gene in range(i, j):
        child[center_parent_gene] = center_parent.permutation[center_parent_gene]
        used_numbers.append(center_parent.permutation[center_parent_gene])

    # dodajemy lewy i prawy brzeg drugiego rodzica w kolejności występowania liczb, których nie ma w środku dziecka
    child_index = 0
    for number in border_parent.permutation:
        if number not in used_numbers:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child[child_index] = number
                child_index += 1
                used_numbers.append(number)

    return child


# mutacja osobników, %-owa szansa na wykonanie inwersji losowych indeksów
def mutation(graph, generation, mutation_prob, i, j):
    for temp_chromosome in generation:
        rand = random.random()
        if rand < mutation_prob:
            generation.append((inversion(temp_chromosome[0], i, j), calc_dist(graph, temp_chromosome[0])))
            generation.remove(temp_chromosome)
    return generation


def inversion(permutation, i, j):
    while i < j:
        permutation[i], permutation[j] = permutation[j], permutation[i]
        i += 1
        j -= 1
    return permutation


# główna funkcja
def genetic(graph, population_size, mutation_prob, number_of_iterations):
    best_solution = None
    best_solution_distance = 0

    generation = generate_start_population(graph, population_size)
    for temp_chr in generation:
        if best_solution is None or temp_chr[1] < best_solution_distance:
            best_solution, best_solution_distance = temp_chr[0], temp_chr[1]

    for i in range(number_of_iterations):
        selected_parents = selection(generation, population_size)

        crossover_i = math.floor(population_size / 3)
        crossover_j = math.floor(population_size * 2 / 3)
        new_generation = crossover(graph, selected_parents, crossover_i, crossover_j)

        mutation_inversion_i = random.randint(0, graph.number_of_nodes() - 1)
        mutation_inversion_j = random.randint(0, graph.number_of_nodes() - 1)
        new_generation = mutation(graph, new_generation, mutation_prob, mutation_inversion_i, mutation_inversion_j)

        generation = new_generation

        for temp_chr in generation:
            if temp_chr[1] < best_solution_distance:
                best_solution, best_solution_distance = temp_chr[0], temp_chr[1]

        i += 1

    return best_solution, best_solution_distance
