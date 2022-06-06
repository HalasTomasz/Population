import base_func
import genetic
import time
import tsplib95
import os
import glob
import json


"""
Pomysły na testy
1) Test zbieżnoci -> puscic 2 razy na dwolonej metodzie (select plus cross_over razy 6) graf 300 i pokazać ze total cost
   maleje po 1000 iteracji
2) Test na znajdowanie najktrószej ciezki w zaleznosci od iloci iteracji od 200 do 10000 -> grafy 50 - 300 2 razy
3) Test na  zwiększoną mutacje?? Jak?
4) miasta test?

Niech testy zapisują wyniki do pliku od razu po skończeniu danego algorytmu, a nie na sam koniec (dla wygody zbierania 
wyników)
3): Np na tym samym grafie co w 1) zwiększajmy/zmniejszajmy % mutacji (np. o 0.05 z 6 razy)
4): Może być tak jak zazwyczaj, czyli dla kilku wybranych miast posprawdzać, możemy tutaj np nie bawić się w zwiększanie 
    mutacji czy iteracji
tylko uzależnić je od rozmiaru grafu (np dla grafu o rozmiarze n niech liczba mutacji wyjdzie coś w stylu 1/n, a liczba 
iteracji załóżmy n^2 / 2)
i dla tych argumentów parę razy puścić
Możemy tutaj ograniczyć się z metodami np używając tych które dawały lepsze wyniki w teście 1) żeby nie trwało za długo

Możemy w kodzie jeszcze zmienić taką zależność, żeby warunkiem końca nie była liczba iteracji, lecz czas (jeśli okaże
się, że algorytmy za długo będą chodzić, to może dużo przyspieszyć, a wyniki nie powinny aż tak odstawać
"""

"""
TO DO 
THNIK ABOUT
"""

# "random" , "roul" , "tour"
# "order_crossover", "mapped_crossover"


def DataMutex(Type, sel_cross, t, solution, permutation, n, ite, mutex):
    Dic = {
        'Type': Type,
        'type_of': sel_cross,
        'time': t,
        'solution': solution,
        'permutation': permutation,
        'size_of_graph': n,
        'iteation': ite,
        'mutex': mutex
        # 'memory'

    }
    return Dic


def test_nr_mutex():
    types = ['sym', 'asym', 'eu']
    collection = []
    mutation_table = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    seed = 100
    size = 100

    graph_sym = base_func.generate_graph(size, seed, 'sym')
    graph_asym = base_func.generate_graph(size, seed, 'asym')
    graph_eu = base_func.generate_graph(size, seed, 'eu')

    for i in range(2):  # 10
        for type_of_graph in types:
            for iteration in range(100, 201, 100):  # liczba iteracji
                for mutation in mutation_table:

                    if type_of_graph == "sym":

                        graph = graph_sym

                    elif type_of_graph == "eu":

                        graph = graph_eu

                    else:
                        graph = graph_asym

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "roul",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'roul' + " order", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "random",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "tour",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    ##############################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "roul",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'roul' + " map", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "random",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'rand' + " map", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "tour",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'tour' + " map", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    ###########################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "roul",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'roul' + " cycle", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "random",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'rand' + " cycle", end - start, cost, str(permutation), size, itera,
                                  mutation))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, size ** 2, mutation, iteration, "tour",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataMutex(type_of_graph, 'tour' + " cycle", end - start, cost, str(permutation), size, itera,
                                  mutation))

    try:
        file = open("Mutation Test2", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()


def Data(Type, sel_cross, t, solution, permutation, n, ite):
    Dic = {
        'Type': Type,
        'type_of': sel_cross,
        'time': t,
        'solution': solution,
        'permutation': permutation,
        'size_of_graph': n,
        'iteation': ite
        # 'memory'

    }
    return Dic


def test_path():
    types = ['sym', 'asym', 'eu']
    collection = []

    seed = 100
    # Incerase Number of Popualtion?
    for i in range(3):  # 10
        for type_of_graph in types:
            for iteration in range(100, 1001, 100):  # liczba iteracji
                for graph_size in range(50, 300, 20):
                    graph = base_func.generate_graph(graph_size, seed, type_of_graph)

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "roul",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'roul' + " order", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "random",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "tour",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'tour' + " order", end - start, cost, str(permutation), graph_size, itera))

                    ##############################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "roul",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'roul' + " map", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "random",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'rand' + " map", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "tour",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'tour' + " map", end - start, cost, str(permutation), graph_size, itera))

                    ###########################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "roul",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'roul' + " cycle", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "random",
                                                        "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'rand' + " cycle", end - start, cost, str(permutation), graph_size, itera))

                    start = time.process_time()

                    permutation, cost = genetic.genetic(graph, graph_size ** 2, 0.1, iteration, "tour",
                                                        "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        Data(type_of_graph, 'tour' + " cycle", end - start, cost, str(permutation), graph_size, itera))

    try:
        file = open("Data Test", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()


def test_city(path):
    print(path)
    collection = []
    file_number = 0
    mutation_table = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    for filename in os.listdir(path):
        file_number += 1
        if file_number > 10:
            break

        path_to_folder = path + "/" + filename
        path_to_tsp = r"" + path + "/" + filename + '/' + filename
        answer = set([os.path.dirname(p) for p in glob.glob(path_to_folder + "/*/*")])

        assert os.path.isfile(path_to_tsp)
        with open(path_to_tsp, "r") as f:

            print("Solving :" + filename)
            problem = tsplib95.read(f)
            graph = problem.get_graph()
            graph = graph.to_directed()

            if answer:
                path_to_tour = path_to_folder + "/" + filename.split('.')[0] + ".opt.tour" + "/" + filename.split('.')[
                    0] + ".opt.tour"
                opt = tsplib95.load(path_to_tour)
                opt = problem.trace_tours(opt.tours)
                print("Rozwiązanie optymalne: ", opt)
            else:
                opt = "None"

            for pop_size in range(graph.number_of_nodes(), 2 * pow(graph.number_of_nodes(), 2), 300):
                for mutation in mutation_table:
                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "roul",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'roul' + " order", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "random",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'rand' + " order", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "tour",
                                                               "order_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'rand' + " order", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    ##############################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "roul",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'roul' + " map", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "random",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'rand' + " map", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "tour",
                                                               "mapped_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'tour' + " map", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    ###########################################################################################

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "roul",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'roul' + " cycle", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "random",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'rand' + " cycle", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

                    start = time.process_time()

                    permutation, cost, itera = genetic.genetic(graph, pop_size, mutation, 1000, "tour",
                                                               "cycle_crossover", start)

                    end = time.process_time()

                    collection.append(
                        DataCity(filename, 'tour' + " cycle", end - start, cost, str(permutation),
                                 graph.number_of_nodes(), itera, mutation, opt))

    try:
        with open('City', 'w') as fout:
            json.dump(collection, fout)
    except IOError:
        pass
    finally:
        fout.close()


"""
dic to save data to JSON 
"""


def DataCity(Type, func, t, solution, permutation, n, iterations, mutation, opt):
    Dic = {
        'Type': Type,
        'function': func,
        'time': t,
        'solution': solution,
        'perm': permutation,
        'size_of_graph': n,
        'iter': iterations,
        'mutation': mutation,
        'optimal_solution': opt
        # 'memory'

    }
    return Dic

# def DataCov(Type, sel_cross, solution, total, n, ite, people):
#     Dic = {
#             'Type': Type,
#             'type_of': sel_cross,
#             'solution': solution,
#             'total_cost': total,
#             'size_of_graph': n,
#             'iteation':ite,
#             'people': people
#             # 'memory'

#         }
#     return Dic

# def Test_cov():

#     types = ['sym']
#     collection = []

#     seed=100
#     # Incerase Number of Popualtion?
#     for type_of_graph in types:
#         for iteration in range(100,1001,100): # liczba iteracji
#             for graph_size in  range(50,200,50):
#                 for  popualtion in range(200,2 *graph_size**2, 400)
#                     graph = base_func.generate_graph(graph_size, seed, type_of_graph)
#                  #GET THE LIST OF TOTAL COST DURING ITERATIONS

#                     permutation, cost = genetic.genetic(graph, popualtion, 0.1, iteration, "roul", "order_crossover")


#                     collection.append(
#                                 DataCov(type_of_graph, 'roul' + " order", cost , total_cost, graph_size,iteration))


                      # permutation, cost = genetic.genetic(graph, popualtion, 0.1, iteration, "random",
                      #                                     "order_crossover")


#                     collection.append(
#                                 DataCov(type_of_graph, 'rand' + " order", cost , total_cost, graph_size,iteration))


#                     permutation, cost = genetic.genetic(graph, popualtion, 0.1, iteration, "tour", "order_crossover")


#                     collection.append(
#                                 DataCov(type_of_graph, 'tour' + " order", cost , total_cost, graph_size,iteration))


#     try:
#         file = open("Data Test", "w")
#         json.dump(collection, file, indent=3)
#     except IOError:
#         pass
#     finally:
#         file.close()
