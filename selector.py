import random


def uni_parent():
    global population_size, list_of_humans, selected_parents
    i = 0
    while i != population_size:  # Moze by orgraniczyć liczbe rozmnażania?
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
lekko zredagowany do bieżących potrzeb
"""


# selekcja rodziców, niektórzy się powtarzają, niektórzy mogą się nie powtórzyć
# ruletka
def roul_parent():
    global population_size, total_cost, list_of_humans, total_adapt_points, selected_parents

    roulette_compartment = 0.0
    for human in list_of_humans:
        roulette_prob = (total_cost / (human.dis * total_adapt_points))
        human.set_roulette(roulette_prob, roulette_compartment, roulette_compartment + roulette_prob)

        roulette_compartment += roulette_prob  # CZY TO ŻE TABLICA LUDZI JEST POSORTOWANA COS ZMIENIA?

    for i in range(population_size):
        first_parent = get_parent(random.random())
        second_parent = get_parent(random.random())
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


def a():
    return None
