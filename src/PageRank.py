from src.utils import init_graph

def PageRank_one_iter(graph, d):
    node_list = graph.nodes
    for node in node_list:
        node.update_pagerank(d, len(graph.nodes))
    graph.normalize_pagerank()

def PageRank(graph, d, iteration=100, save_iterations='no'):
    for i in range(iteration):
        if save_iterations == 'yes':
            graph.add_iteration_pagerank()
        PageRank_one_iter(graph, d)

if __name__ == '__main__':

    iteration = 100
    damping_factor = 0.85

    graph = init_graph('./data/graph_1.txt')

    PageRank(iteration, graph, damping_factor)
    print(graph.get_pagerank_list())