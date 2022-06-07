import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import json


def plotting(filename):
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
        type_of_selections = [i["type_of"] for i in data_type]
        times = [i["time"] for i in data_type]
        solutions = [i["solution"] for i in data_type]
        iterations = [i["iteration"] for i in data_type]
        mutations = [i["mutex"] for i in data_type]
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
            sns.lineplot(data=new_query, x='mutations', y='solutions_mean', hue='type_of_selections')
            plt.title(f"Zależność rozwiązania od procentowej mutacji dla grafu {data_type[0]['Type']} 100 i czasu"
                      f"{algorithm_time}")
            plt.show()
            plt.clf()

        for mutation in np.unique(mutations):
            new_query = df_iterations.query(f"mutations == {mutation}")
            print(new_query)
            sns.lineplot(data=new_query, x='times', y='iterations_mean', hue='type_of_selections')
            plt.title(f"Zależność liczby iteracji od czasu trwania algorytmu dla grafu {data_type[0]['Type']} 100 i"
                      f"mutacji {mutation}")
            plt.show()
            plt.clf()
