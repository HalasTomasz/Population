import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import json


def plotting_mutation_test(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    types = [sym_data, asym_data, full_data, eu_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        type_of_selections = [i["type_of"] for i in data_type if i["iteration"] > 0]
        times = [i["time"] for i in data_type if i["iteration"] > 0]
        solutions = [i["solution"] for i in data_type if i["iteration"] > 0]
        iterations = [i["iteration"] for i in data_type if i["iteration"] > 0]
        mutations = [i["mutex"] for i in data_type if i["iteration"] > 0]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'times': times, 'solutions': solutions,
                           'iterations': iterations, 'mutations': mutations})

        df_mutations = df.groupby(['type_of_selections', 'times', 'mutations']).agg({'solutions': ['mean']})
        df_mutations.columns = ['solutions_mean']
        df_mutations = df_mutations.reset_index()

        df_iterations = df.groupby(['type_of_selections', 'times', 'mutations']).agg({'iterations': ['mean']})
        df_iterations.columns = ['iterations_mean']
        df_iterations = df_iterations.reset_index()

        for algorithm_time in np.unique(times):
            new_query = df_mutations.query(f"times == {algorithm_time}")
            print(new_query)
            sns.barplot(data=new_query, x='type_of_selections', y='solutions_mean', hue='mutations')
            plt.title(f"Zależność rozwiązania od procentowej mutacji dla grafu {data_type[0]['Type']}"
                      f"{data_type[0]['size_of_graph']} i czasu {algorithm_time}")
            plt.show()
            plt.clf()

            new_query = df_iterations.query(f"times == {algorithm_time}")
            print(new_query)
            sns.barplot(data=new_query, x='type_of_selections', y='iterations_mean', hue='mutations')
            plt.title(f"Zależność liczby iteracji od czasu trwania algorytmu dla grafu {data_type[0]['Type']}"
                      f"{data_type[0]['size_of_graph']} i czasu {algorithm_time}")
            plt.show()
            plt.clf()

        # for mutation in np.unique(mutations):
        #     new_query = df_iterations.query(f"mutations == {mutation}")
        #     print(new_query)
        #     sns.barplot(data=new_query, x='type_of_selections', y='iterations_mean', hue='times')
        #     plt.title(f"Zależność liczby iteracji od czasu trwania algorytmu dla grafu {data_type[0]['Type']}"
        #               f"{data_type[0]['size_of_graph']} i mutacji {mutation}")
        #     plt.show()
        #     plt.clf()


def plotting_data_test(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    types = [sym_data, asym_data, full_data, eu_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        type_of_selections = [i["type_of"] for i in data_type if i["iteration"] > 0]
        times = [i["time"] for i in data_type if i["iteration"] > 0]
        solutions = [i["solution"] for i in data_type if i["iteration"] > 0]
        graph_sizes = [i["size_of_graph"] for i in data_type if i["iteration"] > 0]
        iterations = [i["iteration"] for i in data_type if i["iteration"] > 0]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'times': times, 'solutions': solutions,
                           'graph_sizes': graph_sizes, 'iterations': iterations})

        df_solutions = df.groupby(['type_of_selections', 'times', 'graph_sizes']).agg({'solutions': ['mean']})
        df_solutions.columns = ['solutions_mean']
        df_solutions = df_solutions.reset_index()

        df_iterations = df.groupby(['type_of_selections', 'times', 'graph_sizes']).agg({'iterations': ['mean']})
        df_iterations.columns = ['iterations_mean']
        df_iterations = df_iterations.reset_index()

        for graph_size in np.unique(graph_sizes):
            new_query = df_solutions.query(f"graph_sizes == {graph_size}")
            print(new_query)
            sns.barplot(data=new_query, x='type_of_selections', y='solutions_mean', hue='times')
            plt.title(f"Zależność rozwiązania od czasu trwania algorytmu dla grafu {data_type[0]['Type']}{graph_size}")
            plt.show()
            plt.clf()

        # for algorithm_time in np.unique(times):
        #     new_query = df_solutions.query(f"times == {algorithm_time}")
        #     print(new_query)
        #     sns.lineplot(data=new_query, x='graph_sizes', y='solutions_mean', hue='type_of_selections')
        #     plt.title(f"Zależność rozwiązania od rozmiaru grafu dla grafu {data_type[0]['Type']} i "
        #               f"czasu {algorithm_time}")
        #     plt.show()
        #     plt.clf()

        for graph_size in np.unique(graph_sizes):
            new_query = df_iterations.query(f"graph_sizes == {graph_size}")
            print(new_query)
            sns.barplot(data=new_query, x='type_of_selections', y='iterations_mean', hue='times')
            plt.title(f"Zależność liczby iteracji od czasu trwania algorytmu dla grafu {data_type[0]['Type']}"
                      f"{graph_size}")
            plt.show()
            plt.clf()


def plotting_city_test(filename):
    data = json.load(open(filename, "r"))

    types = {
        "bays29.tsp": [],
        "berlin52.tsp": [],
        "ch130.tsp": [],
        "ch150.tsp": [],
        "eil101.tsp": [],
        "eil51.tsp": [],
        "eil76.tsp": [],
        "gr120.tsp": []
    }
    for element in data:
        types[element["Type"]].append(element)

    for data_type in types:
        type_of_selections = [i["function"] for i in types[data_type]]
        solutions = [i["solution"] for i in types[data_type]]
        graph_sizes = [i["size_of_graph"] for i in types[data_type]]
        population_sizes = [i["population_size"] for i in types[data_type]]
        iterations = [i["iter"] for i in types[data_type]]
        mutations = [i["mutation"] for i in types[data_type]]
        optimal_solutions = [i["optimal_solution"] for i in types[data_type]]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'solutions': solutions,
                           'graph_sizes': graph_sizes, 'population_sizes': population_sizes, 'iterations': iterations,
                           'mutations': mutations, 'optimal_solutions': optimal_solutions})

        df_solution = df.groupby(['type_of_selections']).agg({'solutions': ['mean']})
        df_solution.columns = ['solutions_mean']
        df_solution = df_solution.reset_index()

        df_mutation = df.groupby(['type_of_selections', 'mutations']).agg({'solutions': ['mean']})
        df_mutation.columns = ['solutions_mean']
        df_mutation = df_mutation.reset_index()

        df_population = df.groupby(['type_of_selections', 'population_sizes']).agg({'solutions': ['mean']})
        df_population.columns = ['solutions_mean']
        df_population = df_population.reset_index()

        plot = sns.barplot(data=df_solution, x='type_of_selections', y='solutions_mean')
        plot.axhline(optimal_solutions[0], color="black")
        plot.bar_label(plot.containers[0])
        plt.title(f"Średnia rozwiązań dla grafu {data_type}")
        plt.show()
        plt.clf()

        plot = sns.barplot(data=df_mutation, x='type_of_selections', y='solutions_mean', hue='mutations')
        plot.axhline(optimal_solutions[0], color="black")
        for container in plot.containers:
            plot.bar_label(container)
        plt.title(f"Zależność rozwiązania od procentowej mutacji dla grafu {data_type}")
        plt.show()
        plt.clf()

        plot = sns.barplot(data=df_population, x='type_of_selections', y='solutions_mean', hue='population_sizes')
        plot.axhline(optimal_solutions[0], color="black")
        for container in plot.containers:
            plot.bar_label(container)
        plt.title(f"Zależność rozwiązania od rozmiaru populacji dla grafu {data_type}")
        plt.show()
        plt.clf()


def plotting_unique_test(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    # types = [sym_data, asym_data, full_data, eu_data]
    types = [sym_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        type_of_selections = [i["type_of"] for i in data_type if i["iteration"] > 0]
        times = [i["time"] for i in data_type if i["iteration"] > 0]
        solutions = [i["solution"] for i in data_type if i["iteration"] > 0]
        iterations = [i["iteration"] for i in data_type if i["iteration"] > 0]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'times': times, 'solutions': solutions,
                           'iterations': iterations})

        plot = sns.barplot(data=df, x='type_of_selections', y='solutions', hue='times')
        for container in plot.containers:
            plot.bar_label(container)
        plt.title(f"Zależność rozwiązania od czasu dla grafu {data_type[0]['Type']}100, mutacji 0.1, populacji 10000")
        plt.show()
        plt.clf()


def plotting_cost_test(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    # types = [sym_data, asym_data, full_data, eu_data]
    types = [sym_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        type_of_selections = [i["type_of"] for i in data_type if i["iteration"] > 0]
        solutions = [i["solution"] for i in data_type if i["iteration"] > 0]
        total_costs = [i["total_cost"] for i in data_type if i["iteration"] > 0]
        iterations = [i["iteration"] for i in data_type if i["iteration"] > 0]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'solutions': solutions, 'total_costs': total_costs,
                           'iterations': iterations})

        sns.lineplot(x=range(1, iterations[1] + 2), y=total_costs[1])
        plt.title(f"Zależność łącznego kosztu permutacji od iteracji")
        plt.show()
        plt.clf()


def plotting_cost2_test(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    # types = [sym_data, asym_data, full_data, eu_data]
    types = [sym_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        type_of_selections = [i["type_of"] for i in data_type if i["iteration"] > 0]
        solutions = [i["solution"] for i in data_type if i["iteration"] > 0]
        total_costs = [i["total_cost"] for i in data_type if i["iteration"] > 0]
        iterations = [i["iteration"] for i in data_type if i["iteration"] > 0]
        populations = [i["people"] for i in data_type if i["iteration"] > 0]
        df = pd.DataFrame({'type_of_selections': type_of_selections, 'solutions': solutions, 'total_costs': total_costs,
                           'iterations': iterations, 'populations': populations})

        # colors = ['r', 'g', 'b']
        # sns.set_palette("PuBuGn_d")
        for i in range(3):
            sns.lineplot(x=range(1, iterations[i] + 2), y=total_costs[i], label=str(populations[i]))
            plt.title(f"Zależność łącznego kosztu permutacji od iteracji")
        plt.legend()
        plt.show()
        plt.clf()
