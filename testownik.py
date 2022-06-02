
"""
Pomysły na testy
1) Test zbieżnoci -> puscic 2 razy na dwolonej metodzie (select plus cross_over razy 6) graf 300 i pokazać ze total cost maleje po 1000 iteracji
2) Test na znajdowanie najktrószej ciezki w zaleznosci od iloci iteracji od 200 do 10000 -> grafy 50 - 300 2 razy
3) Test na  zwiększoną mutacje?? Jak?
4) miasta test?

Niech testy zapisują wyniki do pliku od razu po skończeniu danego algorytmu, a nie na sam koniec (dla wygody zbierania wyników)
3): Np na tym samym grafie co w 1) zwiększajmy/zmniejszajmy % mutacji (np. o 0.05 z 6 razy)
4): Może być tak jak zazwyczaj, czyli dla kilku wybranych miast posprawdzać, możemy tutaj np nie bawić się w zwiększanie mutacji czy iteracji
tylko uzależnić je od rozmiaru grafu (np dla grafu o rozmiarze n niech liczba mutacji wyjdzie coś w stylu 1/n, a liczba iteracji załóżmy n^2 / 2)
i dla tych argumentów parę razy puścić
Możemy tutaj ograniczyć się z metodami np używając tych które dawały lepsze wyniki w teście 1) żeby nie trwało za długo

Możemy w kodzie jeszcze zmienić taką zależność, żeby warunkiem końca nie była liczba iteracji, lecz czas (jeśli okaże
się, że algorytmy za długo będą chodzić, to może dużo przyspieszyć, a wyniki nie powinny aż tak odstawać
"""

"""
TO DO 
THNIK ABOUT
"""
import base_func
import genetic
import time
import json
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
            'iteation':ite,
            'mutex': mutex
            # 'memory'

        }
    return Dic

def test_nr_mutex():
    
    types = ['sym', 'asym', 'eu']
    collection = []
    mutex = [0.05, 0.1, 0.15,0.2, 0.3, 0.5]
    seed=100
    size = 250
    
    graph_sym = genetic.genetic(size, seed, 'sym')
    graph_asym = genetic.genetic(size, seed, 'asym')
    graph_eu = genetic.genetic(size, seed, 'eu')

    for i in range(3): # 10
        for type_of_graph in types:
            for iteration in range(100,901,100): # liczba iteracji
                for mutation in mutex:

                    if  type_of_graph == "sym":
                        
                        graph = graph_sym
                        
                    elif type_of_graph == "eu":
                        
                        graph = graph_eu
                        
                    else:
                        graph = graph_asym
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "roul", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'roul' + " order", end - start, cost, str(permutation), size,iteration,mutation))
                    
              
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "random", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), size,iteration,mutation))
                    
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "tour", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), size,iteration,mutation))
                    
                    ##############################################################################################
                        
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "roul", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'roul' + " map", end - start, cost, str(permutation), size,iteration,mutation))
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "random", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'rand' + " map", end - start, cost, str(permutation), size,iteration,mutation))
                    
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, mutation, iteration, "tour", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                DataMutex(type_of_graph, 'rand' + " map", end - start, cost, str(permutation), size,iteration,mutation))
                    
                    ###########################################################################################
                    
                      
    try:
        file = open("Mutex Test", "w")
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
            'iteation':ite
            # 'memory'

        }
    return Dic

def test_path():
      
    types = ['sym', 'asym', 'eu']
    collection = []

    seed=100
    # Incerase Number of Popualtion?
    for i in range(3): # 10
        for type_of_graph in types:
            for iteration in range(100,1001,100): # liczba iteracji
                for graph_size in  range(50,300,20):

                    graph = base_func.generate_graph(graph_size, seed, type_of_graph)
                
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "roul", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'roul' + " order", end - start, cost, str(permutation), graph_size,iteration))
                    
              
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "random", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'rand' + " order", end - start, cost, str(permutation), graph_size,iteration))
                    
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "tour", "order_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'tour' + " order", end - start, cost, str(permutation), graph_size,iteration))
                    
                    ##############################################################################################
                        
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "roul", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'roul' + " map", end - start, cost, str(permutation), graph_size,iteration))
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "random", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'rand' + " map", end - start, cost, str(permutation), graph_size,iteration))
                    
                    
        
                    start = time.process_time()
        
                    permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "tour", "mapped_crossover")
        
                    end = time.process_time()
        
                    collection.append(
                                Data(type_of_graph, 'tour' + " map", end - start, cost, str(permutation), graph_size,iteration))
                    
                    ###########################################################################################
                    
                      
    try:
        file = open("Data Test", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()

def DataCov(Type, sel_cross, solution, total, n, ite):
    Dic = {
            'Type': Type,
            'type_of': sel_cross,
            'solution': solution,
            'total_cost': total,
            'size_of_graph': n,
            'iteation':ite
            # 'memory'

        }
    return Dic

def Test_cov():
      
    types = ['sym']
    collection = []

    seed=100
    # Incerase Number of Popualtion?
    for type_of_graph in types:
        for iteration in range(100,1001,100): # liczba iteracji
            for graph_size in  range(50,200,50):

                graph = base_func.generate_graph(graph_size, seed, type_of_graph)
             #GET THE LIST OF TOTAL COST DURING ITERATIONS
    
                permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "roul", "order_crossover")
    
    
                collection.append(
                            DataCov(type_of_graph, 'roul' + " order", cost , total_cost, graph_size,iteration))
                
          
                permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "random", "order_crossover")
    
                
                collection.append(
                            DataCov(type_of_graph, 'rand' + " order", cost , total_cost, graph_size,iteration))
                
                
    
                permutation, cost = genetic.genetic(graph, 100, 0.1, iteration, "tour", "order_crossover")
    
    
                collection.append(
                            DataCov(type_of_graph, 'tour' + " order", cost , total_cost, graph_size,iteration))
                
                  
    try:
        file = open("Data Test", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()