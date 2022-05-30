import math
import random
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
    list_of_humans.sort(key=lambda x: x.dis)  # testownik sortowanie dla elit   

    i = 0
    for x in list_of_humans:
        x.set_human_id(i)  ### elity
        x.set_adaption_point(x.dis / total_cost)  # Premiowanie  słabyszch?
        total_adapt_points += x.adap_points
        i = i + 1

    # selekcja rodziców, niektórzy się powtarzają, niektórzy mogą się nie powtórzyć


# ruletka
"""
Możliwosc rozbudowy selekcji
"""


def selection(base='roul'):
    if base == 'roul':
        return roul_parent()
    else:
        return uni_parent()


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
    while i != 30:  # Moze by orgraniczyć liczbe rozmnażania?
        first_parent = random.randint(0, population_size - 1)
        second_parent = random.randint(0, population_size - 1)
        if first_parent == second_parent:  # sam ze soba sie nie  moze XDD
            continue
        list_of_humans[first_parent].set_coparent(second_parent)
        list_of_humans[second_parent].set_coparent(first_parent)
        selected_parents.add(first_parent)
        selected_second_parents.add(second_parent)
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
        roulette_prob = (total_cost / (human.dis * total_adapt_points))
        human.set_roulette(roulette_prob, roulette_compartment, roulette_compartment + roulette_prob)

        roulette_compartment += roulette_prob  # CZY TO ŻE TABLICA LUDZI JEST POSORTOWANA COS ZMIENIA?

    for i in range(30):
        first_parent = get_parent(random.random())
        second_parent = get_parent(random.random())
        list_of_humans[first_parent].set_coparent(second_parent)
        list_of_humans[second_parent].set_coparent(first_parent)
        selected_parents.add(first_parent)
        # selected_second_parents.add(second_parent)


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


def crossover(graph, i, j):
    global selected_parents, list_of_humans

    new_generation = []
    # generujemy parę dzieci dla każdej pary rodziców
    for parent in selected_parents:

        while list_of_humans[parent].is_empty_partners_array():
            first_child, second_child = get_child(graph, parent, i, j)

            new_generation.append(Human(first_child, calc_dist(graph, first_child), 0))
            new_generation.append(Human(second_child, calc_dist(graph, second_child), 0))

    return mutation(graph, new_generation)


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
    for number in list_of_humans[first_parent].perm:
        if number not in used_numbers:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child[child_index] = number
                child_index += 1
                used_numbers.append(number)

    child_index = 0
    for number in list_of_humans[sec_parent].perm:
        if number not in used_numbers2:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child2[child_index] = number
                child_index += 1
                used_numbers2.append(number)
    return child, child2


def partially_mapped_crossover(graph, i, j):
    global selected_parents, list_of_humans
    new_generation = []
    # generujemy parę dzieci dla każdej pary rodziców
    for parent in selected_parents:

        while list_of_humans[parent].is_empty_partners_array():
            first_child, second_child = get_child_partially_mapped(graph, parent, i, j)

            new_generation.append(Human(first_child, calc_dist(graph, first_child), 0))
            new_generation.append(Human(second_child, calc_dist(graph, second_child), 0))

    return mutation(graph, new_generation)


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
        child[center_parent_gene] = first_gene
        child2[center_parent_gene] = second_gene

        mapping[first_gene] = second_gene
        mapping2[second_gene] = first_gene

        used_numbers.append(first_gene)
        used_numbers2.append(second_gene)

    child_index = 0
    for number in list_of_humans[first_parent].perm:
        if number not in used_numbers:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child[child_index] = number
                child_index += 1
                used_numbers.append(number)
        else:
            new_number = mapping[number]
            while new_number in used_numbers:
                new_number = mapping[new_number]
            child[child_index] = number
            child_index += 1
            used_numbers.append(number)

    child_index = 0
    for number in list_of_humans[sec_parent].perm:
        if number not in used_numbers2:
            if child_index == i:
                child_index = j
            if child_index < graph.number_of_nodes():
                child2[child_index] = number
                child_index += 1
                used_numbers2.append(number)
        else:
            new_number = mapping2[number]
            while new_number in used_numbers2:
                new_number = mapping2[new_number]
            child2[child_index] = number
            child_index += 1
            used_numbers2.append(number)

    return child, child2


# mutacja osobników, %-owa szansa na wykonanie inwersji losowych indeksów
"""
Mutacja lecz wykorzystuej kalsy
"""


def mutation(graph, generation):
    global total_cost, list_of_humans

    i = random.randint(0, graph.number_of_nodes() - 1)
    j = random.randint(0, graph.number_of_nodes() - 1)
    # punkty losowane dla kazdego !!!

    total_cost = 0  ## UWAGA MOZE NIE DZIAŁAĆ INNCYH SELECTEROÓW
    for i in range(len(generation)):

        rand = random.random()
        if rand < mutation_prob:
            generation[i].perm = inversion(generation[i].perm, i, j)
            generation[i].dis = calc_dist(graph, generation[i].perm)
            total_cost += generation[i].dis
        else:
            total_cost += generation[i].dis

    return generation


def final_check():
    global list_of_humans, selected_parents, selected_second_parents

    for i in range(len(list_of_humans)):

        list_of_humans[i].set_adaption_point(list_of_humans[i].dis / total_cost)

        if i in selected_parents or i in selected_second_parents:
            list_of_humans[i].add_age()

    selected_parents = set()
    selected_second_parents = set()


"""
KONIEC SEKCJI CROSS OVER
"""


def kill():
    global total_cost, total_adapt_points, list_of_humans, selected_second_parents, selected_parents

    for human in list_of_humans:

        if human.age == 0:
            total_cost -= human.dis
            total_adapt_points -= human.adap_points
            list_of_humans.remove(human)
        else:
            human.age = 0


"""
KONIEC SEKCJI Zabij itp  
"""


# główna funkcja
def genetic(graph, population_number, mutation_chance, number_of_iterations):
    global list_of_humans, population_size, mutation_prob, total_adapt_points

    best_solution = None
    best_solution_distance = 0
    population_size = population_number
    mutation_prob = mutation_chance

    generate_start_population(graph)  # Now we get list of humans

    # Pick teh best human Avaible

    for i in range(number_of_iterations):
        print("done ", i)
        selection()

        crossover_i = math.floor(graph.number_of_nodes() / 3)
        crossover_j = math.floor(graph.number_of_nodes() * 2 / 3)

        list_of_humans = crossover(graph, crossover_i, crossover_j)  ## POSSIBLE OUT COME

        # generator = crossover(graph, crossover_i, crossover_j)
        # list_of_humans.extend(generator)
        # population_size = len(list_of_humans)
        # final_check()

        list_of_humans.sort(key=lambda x: x.dis)

        population_size = len(list_of_humans)
        i = 0
        for x in list_of_humans:
            x.set_human_id(i)
            x.set_adaption_point(x.dis / total_cost)
            total_adapt_points += x.adap_points
            i = i + 1

        best_solution, best_solution_distance = list_of_humans[-1].perm, list_of_humans[-1].dis

        # if i % 4 == 0 :
        # kill()

    return best_solution, best_solution_distance
