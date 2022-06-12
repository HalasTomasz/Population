import math
import random
import numpy as np
import time
from chromosome import Human
# from selector import uni_parent
from base_func import calc_dist, inversion  # Basic known functions

"""

UWAGI DODAC 2 krzyzowania
PRZYNINAC POPULACJE W INNY SPOSÓB 
"""

"""
Globalne zmienne bardzo często używane w programie
list_of_humans - > populacja / lista obiektów typu Human
population_size -> rozmiar populacji == len(list_of_humans)
total_cost -> całkowity koszt
total_adapt_points -> ???
selected_parents -> zbiór rodziców do komupalcji a konkretniej zawiera wszytskie tylko pierwszych rodziców z pary
mutation_prob - > prawdo mutacji
"""
list_of_humans = []
population_size = 0
total_cost = 0
total_adapt_points = 0
selected_parents = set()
selected_second_parents = set()
mutation_prob = 0
best_solution = []
best_solution_distance = np.inf
"""
Kom Szymon
"""
# generujemy populację początkową (tutaj losowo, można potem wrzucić to w osobną funkcję i generować start przekazując
# funkcję w argumencie
# zwraca słownik: klucz - permutacja, wartość - wartość funkcji celu

"""
Generujemy Popualcje początkowa (losowo) 
uwtorzonego człowieka dodajemy do list_of_humans (utworzylismy obiekt z para perm i dis )
Na bieżąc jest kalkulowany całowity koszt populacji
UWAGA DO ZADANIA ZAWIERA BARDZO CIEKAWY MODUL OPOWIEM WIECEJ PRZYPOMNIJ MI 
"""


def generate_start_population(graph):
    global population_size, total_cost, list_of_humans, total_adapt_points

    populations = []  ### Sprawdzic czy sie opłaca test plus optymalizacja

    for _ in range(population_size):

        permutation = list(range(1, graph.number_of_nodes() + 1))
        random.shuffle(permutation)

        if permutation not in [x[0] for x in populations]:
            list_of_humans.append(Human(permutation, calc_dist(graph, permutation), 0))
            total_cost += list_of_humans[-1].dis

    """
    BARDZO CIEKAWY MODUŁ
    """
    ##  i = 0
    for x in list_of_humans:
        #   x.set_human_id(i)
        x.set_adaption_point(total_cost / x.dis)
        total_adapt_points += x.adap_points
    #  i = i + 1

    # selekcja rodziców, niektórzy się powtarzają, niektórzy mogą się nie powtórzyć


# ruletka
"""
Możliwosc rozbudowy selekcji
"""


def selection(base='roul'):
    if base == 'roul':
        roul_parent()

    elif base == "random":
        uni_parent()

    else:
        tournament()


"""
Check if correct
"""


def tournament():
    global population_size, list_of_humans, selected_parents, selected_second_parents
    i = 0
    while i != population_size // 2:
        number_list = random.sample(range(0, population_size - 1), 5)
        number_list = sorted(number_list, key=lambda x: list_of_humans[x].dis)  # sort by dis
        first = number_list[0]

        number_list = random.sample(range(0, population_size - 1), 5)
        number_list = sorted(number_list, key=lambda x: list_of_humans[x].dis)
        second = number_list[0]

        list_of_humans[first].set_coparent(second)  ## Adiing only the best!
        list_of_humans[second].set_coparent(first)
        selected_parents.add(first)
        i += 1
    # print("Parents  ", selected_parents)


"""
To samo wybierz z roz jendostajnego od 0 do Size -1
Potem parenty
Dodaje do ludzi partnerów aby wiedzieli z kim maja dziecko 
A na końcu 
Dodoaje do seta 1 rodzica
"""


def uni_parent():
    global population_size, list_of_humans, selected_parents, selected_second_parents
    i = 0
    while i != population_size // 2:  # Moze by orgraniczyć liczbe rozmnażania?
        first_parent = random.randint(0, population_size - 1)
        second_parent = random.randint(0, population_size - 1)
        if first_parent == second_parent:  # sam ze soba sie nie  moze XDD
            continue
        list_of_humans[first_parent].set_coparent(second_parent)
        list_of_humans[second_parent].set_coparent(first_parent)
        selected_parents.add(first_parent)
        i += 1


"""
KOD SZYMONA 
lekko zredagowany do bierzących potzreb
"""


# selekcja rodziców, niektórzy się powtarzają, niektórzy mogą się nie powtórzyć
# ruletka
def roul_parent():
    global population_size, total_cost, list_of_humans, total_adapt_points, selected_parents, selected_second_parents

    roulette_compartment = 0.0
    for human in list_of_humans:
        roulette_prob = (total_cost / human.dis) / total_adapt_points
        human.set_roulette(roulette_prob, roulette_compartment, roulette_compartment + roulette_prob)

        roulette_compartment += roulette_prob  # CZY TO ŻE TABLICA LUDZI JEST POSORTOWANA COS ZMIENIA?

    # print(roulette_compartment)

    for i in range(population_size // 2):
        first_parent = get_parent(random.random())
        second_parent = get_parent(random.random())
        # print(first_parent, second_parent)
        list_of_humans[first_parent].set_coparent(second_parent)
        list_of_humans[second_parent].set_coparent(first_parent)
        selected_parents.add(first_parent)


# funkcja pomocnicza, wyciąga wylosowanego rodzica
def get_parent(random_number):
    global list_of_humans
    i = 0
    for parent in list_of_humans:
        if parent.roul_start <= random_number <= parent.roul_finish:
            return i
        i += 1
    return None


"""
KONIEC SEKCJI SELCT
"""

# krzyżowanie osobników - tutaj użyty jest order crossover, dwupunktowy

"""
Cóż to przeszukuje zbiór ten set
znajduje partnera a przez to jego partnera nr 2
wywyslam do funkcji aby generowała obu dzieciaków
na koneic appenduje nowa generacje
"""


def crossover(graph, get_child_function, i, j, method_selected):
    global selected_parents, list_of_humans

    new_generation = []
    # generujemy parę dzieci dla każdej pary rodziców
    for parent in selected_parents:

        while list_of_humans[parent].is_empty_partners_array():
            first_child, second_child = get_child_function(graph, parent, i, j)

            new_generation.append(Human(first_child, calc_dist(graph, first_child), 0))
            new_generation.append(Human(second_child, calc_dist(graph, second_child), 0))

    return mutation(graph, new_generation, method_selected)


"""
Robie dwójke dziecki identycznie jak wczesnie jelcz wykorzystuje kalse do tego 
"""


# pomocnicza funkcja do generowania dziecka
def get_child(graph, parent, i, j):
    global list_of_humans, population_size

    child = [None] * graph.number_of_nodes()
    child2 = [None] * graph.number_of_nodes()

    used_numbers = []
    used_numbers2 = []

    sec_parent = list_of_humans[parent].do_sex()
    first_parent = parent
    list_of_humans[sec_parent].do_remove(first_parent)

    # środek dziecka jest środkiem jednego z rodziców
    for center_parent_gene in range(i, j):
        # print(first_parent,"   ",sec_parent,"   ", len(child), "   ", center_parent_gene, "  ",i,"  ",j )
        child[center_parent_gene] = list_of_humans[first_parent].perm[center_parent_gene]
        child2[center_parent_gene] = list_of_humans[sec_parent].perm[center_parent_gene]

        used_numbers.append(list_of_humans[first_parent].perm[center_parent_gene])
        used_numbers2.append(list_of_humans[sec_parent].perm[center_parent_gene])

    # dodajemy lewy i prawy brzeg drugiego rodzica w kolejności występowania liczb, których nie ma w środku dziecka
    child_index = 0
    for number in list_of_humans[sec_parent].perm:
        if number not in used_numbers:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child[child_index] = number
                child_index += 1
                used_numbers.append(number)

    child_index = 0
    for number in list_of_humans[first_parent].perm:
        if number not in used_numbers2:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child2[child_index] = number
                child_index += 1
                used_numbers2.append(number)
    return child, child2


def get_child_partially_mapped(graph, parent, i, j):
    global list_of_humans, population_size

    child = [None] * graph.number_of_nodes()
    child2 = [None] * graph.number_of_nodes()

    used_numbers = []
    used_numbers2 = []

    sec_parent = list_of_humans[parent].do_sex()
    first_parent = parent
    list_of_humans[sec_parent].do_remove(first_parent)

    mapping = {}
    mapping2 = {}

    # środek dziecka jest środkiem jednego z rodziców
    for center_parent_gene in range(i, j):
        # print(first_parent,"   ",sec_parent,"   ", len(child), "   ", center_parent_gene, "  ",i,"  ",j )
        first_gene = list_of_humans[first_parent].perm[center_parent_gene]
        second_gene = list_of_humans[sec_parent].perm[center_parent_gene]
        child[center_parent_gene] = second_gene
        child2[center_parent_gene] = first_gene

        mapping[second_gene] = first_gene
        mapping2[first_gene] = second_gene

        used_numbers.append(second_gene)
        used_numbers2.append(first_gene)

    child_index = 0
    for number in list_of_humans[first_parent].perm:
        if child_index < i or child_index >= j:
            if number in used_numbers:
                new_number = mapping[number]
                while new_number in used_numbers:
                    new_number = mapping[new_number]
                child[child_index] = new_number
            else:
                child[child_index] = number
        child_index += 1

    child_index = 0
    for number in list_of_humans[sec_parent].perm:
        if child_index < i or child_index >= j:
            if number in used_numbers2:
                new_number = mapping2[number]
                while new_number in used_numbers2:
                    new_number = mapping2[new_number]
                child2[child_index] = new_number
            else:
                child2[child_index] = number
        child_index += 1

    return child, child2


def get_child_cycle(graph, parent, i, j):
    global list_of_humans, population_size

    child = [None] * graph.number_of_nodes()
    child2 = [None] * graph.number_of_nodes()

    used_numbers = []
    used_numbers2 = []

    mapping = {}
    mapping2 = {}

    sec_parent = list_of_humans[parent].do_sex()
    first_parent = parent
    list_of_humans[sec_parent].do_remove(first_parent)

    for i in range(len(child)):
        first_gene = list_of_humans[first_parent].perm[i]
        second_gene = list_of_humans[sec_parent].perm[i]

        mapping[first_gene] = second_gene
        mapping2[second_gene] = first_gene

    i = 0
    used_parent = first_parent
    used_mapping = mapping
    while i < len(child):
        first_gene = list_of_humans[used_parent].perm[i]
        second_gene = used_mapping[first_gene]

        if child[i] is None:
            child[i] = first_gene
            used_numbers.append(first_gene)

            while second_gene not in used_numbers:
                first_gene = second_gene
                second_gene = used_mapping[first_gene]
                index = list_of_humans[used_parent].perm.index(first_gene)

                if child[index] is None:
                    child[index] = first_gene
                    used_numbers.append(first_gene)
            used_mapping = mapping2 if used_mapping == mapping else mapping
            used_parent = first_parent if used_parent == sec_parent else sec_parent
        i += 1

    i = 0
    used_parent = sec_parent
    used_mapping = mapping2
    while i < len(child2):
        first_gene = list_of_humans[used_parent].perm[i]
        second_gene = used_mapping[first_gene]

        if child2[i] is None:
            child2[i] = first_gene
            used_numbers2.append(first_gene)

            while second_gene not in used_numbers2:
                first_gene = second_gene
                second_gene = used_mapping[first_gene]
                index = list_of_humans[used_parent].perm.index(first_gene)

                if child2[index] is None:
                    child2[index] = first_gene
                    used_numbers2.append(first_gene)
            used_mapping = mapping2 if used_mapping == mapping else mapping
            used_parent = first_parent if used_parent == sec_parent else sec_parent
        i += 1

    return child, child2


# mutacja osobników, %-owa szansa na wykonanie inwersji losowych indeksów
"""
Mutacja lecz wykorzystuej kalsy
"""


def mutation(graph, generation, method="roul"):
    global total_cost, selected_parents
    i = random.randint(0, graph.number_of_nodes() - 1)
    j = random.randint(0, graph.number_of_nodes() - 1)

    if method == "roul" or method == "tour":  # NIE ZERUJ GDY POPULACJA SIE PWOIEKSZA A A NIE ZAMIENIA
        total_cost = 0
    for index in range(len(generation)):

        rand = random.random()
        if rand < mutation_prob:
            generation[index].perm = inversion(generation[index].perm, i, j)
            generation[index].dis = calc_dist(graph, generation[index].perm)
            total_cost += generation[index].dis
        else:
            total_cost += generation[index].dis
    selected_parents = set()
    return generation


def final_check():
    global list_of_humans, total_adapt_points, total_cost, best_solution_distance, best_solution

    total_adapt_points = 0
    for i in range(len(list_of_humans)):

        if best_solution_distance > list_of_humans[i].dis:
            best_solution_distance = list_of_humans[i].dis
            best_solution = list_of_humans[i].perm

        list_of_humans[i].set_adaption_point(total_cost / list_of_humans[i].dis)
        total_adapt_points += list_of_humans[i].adap_points


"""
KONIEC SEKCJI CROSS OVER
"""


def kill():
    global total_cost, total_adapt_points, list_of_humans

    for human in list_of_humans:
        human.add_age()
        if human.age == 3:
            total_cost -= human.dis
            list_of_humans.remove(human)


"""
KONIEC SEKCJI Zabij itp  
"""


# główna funkcja
def genetic(graph, population_number, mutation_chance, selection_type, crossover_type,
            start_time, total_time):
    global list_of_humans, population_size, mutation_prob, total_adapt_points, best_solution_distance, best_solution

    list_of_humans = []
    total_adapt_points = 0
    best_solution = []
    best_solution_distance = np.inf

    population_size = population_number
    mutation_prob = mutation_chance

    generate_start_population(graph)  # Now we get list of humans

    i = 0
    while time.process_time() - start_time <= total_time:

        selection(base=selection_type)  # CHANGE THE BASE!

        crossover_i = math.floor(graph.number_of_nodes() / 3)
        crossover_j = math.floor(graph.number_of_nodes() * 2 / 3)

        if crossover_type == "order_crossover":
            list_of_humans = crossover(graph, get_child, crossover_i, crossover_j, selection_type)  # POSSIBLE OUTCOME
        elif crossover_type == "mapped_crossover":
            list_of_humans = crossover(graph, get_child_partially_mapped, crossover_i, crossover_j,
                                       selection_type)  # POSSIBLE OUTCOME
        elif crossover_type == "cycle_crossover":
            list_of_humans = crossover(graph, get_child_cycle, crossover_i, crossover_j, selection_type)

        # generator = crossover(graph, crossover_i, crossover_j)
        # list_of_humans.extend(generator)
        # kill()

        if time.process_time() - start_time > total_time:
            return best_solution, best_solution_distance, i

        final_check()
        population_size = len(list_of_humans)
        i += 1

    return best_solution, best_solution_distance, i
    # i = 0
    # for x in list_of_humans:
    # x.set_human_id(i)
    #  x.set_adaption_point(x.dis / total_cost)
    # total_adapt_points += x.adap_points
    #  i = i + 1

    # best_solution, best_solution_distance = list_of_humans[-1].perm, list_of_humans[-1].dis
