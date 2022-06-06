import re
import time

import genetic
import tsplib95
import testownik

def read_graph_input(file):
    with open(file) as f:
        problem = tsplib95.read(f)

    new_graph = problem.get_graph()
    new_graph = new_graph.to_directed()

    opt = tsplib95.load('bays29.opt.tour')
    print("Optimal: ", problem.trace_tours(opt.tours))
    return new_graph


if __name__ == '__main__':
    # filename = 'bays29.tsp'
    # graph = read_graph_input(filename)
    # population_size = int(re.findall(r'\d+', filename)[0])
    # number_of_iterations = 600
    # mutation_prob = 0.05
    # selection_type = "roul"
    # crossover_type = "mapped_crossover"
    # start_time = time.process_time()
    #
    # solution, solution_distance, iterations = genetic.genetic(graph, population_size, mutation_prob,
    #                                                           number_of_iterations, selection_type, crossover_type,
    #                                                           start_time)
    # print(solution)
    # print(solution_distance)
    
    # testownik.test_nr_mutex()
    testownik.test_city("Data_Meta")
