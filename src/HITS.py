from src.utils import init_graph

def HITS_one_iter(graph):
    node_list = graph.nodes

    for node in node_list:
        node.update_auth()

    for node in node_list:
        node.update_hub()

    graph.normalize_auth_hub()

def HITS(graph, iteration=100, save_iterations='no'):
    for i in range(iteration):
        if save_iterations == 'yes':
            graph.add_iteration_auth_hub()
        HITS_one_iter(graph)
        # graph.display_hub_auth()
        # print()

if __name__ == '__main__':

    iteration = 100

    graph = init_graph('./data/graph_1.txt')
    HITS(iteration, graph)
    auth_list, hub_list = graph.get_auth_hub_list()
    print(auth_list)
    print(hub_list)