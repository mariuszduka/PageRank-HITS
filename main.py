import numpy as np
import os

from src.utils import init_graph
from src.HITS import HITS, HITS_one_iter
from src.PageRank import PageRank, PageRank_one_iter
from optparse import OptionParser

def output_HITS(iteration, graph, result_dir, fname, save_iterations):
    authority_fname = '_HITS_authority.txt'
    authority_iteration_fname = '_HITS_authority_iteration.txt'
    hub_fname = '_HITS_hub.txt'
    hub_iteration_fname = '_HITS_hub_iteration.txt'

    HITS(graph, iteration, save_iterations)
    auth_list, hub_list = graph.get_auth_hub_list()
    auth_list_iteration, hub_list_iteration = graph.get_iteration_auth_hub()

    print()
    print('Authority:')
    print(auth_list)
    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)
    np.savetxt(os.path.join(path, fname + authority_fname), auth_list, fmt='%.3f', newline=" ")
    if save_iterations == 'yes':
        np.savetxt(os.path.join(path, fname + authority_iteration_fname), auth_list_iteration, fmt='%.3f', newline="\n")

    print('Hub:')
    print(hub_list)
    print()
    np.savetxt(os.path.join(path, fname + hub_fname), hub_list, fmt='%.3f', newline=" ")
    if save_iterations == 'yes':
        np.savetxt(os.path.join(path, fname + hub_iteration_fname), hub_list_iteration, fmt='%.3f', newline="\n")

def output_PageRank(iteration, graph, damping_factor, result_dir, fname, save_iterations):
    pagerank_fname = '_PageRank.txt'
    pagerank_iteration_fname = '_PageRank_iteration.txt'

    PageRank(graph, damping_factor, iteration, save_iterations)
    pagerank_list = graph.get_pagerank_list()
    pagerank_iteration = graph.get_iteration_pagerank()

    print('PageRank:')
    print(pagerank_list)
    print()
    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)
    np.savetxt(os.path.join(path, fname + pagerank_fname), pagerank_list, fmt='%.3f', newline=" ")
    if save_iterations == 'yes':
        np.savetxt(os.path.join(path, fname + pagerank_iteration_fname), pagerank_iteration, fmt='%.3f', newline="\n")

def draw_graph_to_file(file_path, result_dir, fname):
    graph_fname = '_graph.png'

    with open(file_path) as f:
        lines = f.readlines()

    G = nx.DiGraph()

    for line in lines:
        t = tuple(line.strip().split(','))
        G.add_edge(*t)

    nx.draw(G, with_labels=True, node_size=2000, edge_color='black', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)

    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)

    plt.savefig(os.path.join(path, fname + graph_fname))

def draw_PageRank_iterations():

    pagerank_iteration = graph.get_iteration_pagerank()
    del pagerank_iteration[0]

    length = len(graph.nodes)
    all_pagerank = [[] for i in range(length)]

    for i in pagerank_iteration:
        for idx, auth in enumerate(i):
            all_pagerank[idx].append(auth)

    y = [int(i) for i in range(1,len(pagerank_iteration)+1)]

    for pagerank_list in all_pagerank:
        plt.plot(y, pagerank_list)

    plt.title('PageRank on iteration')
    plt.legend([node.name for node in graph.nodes])
    plt.xlabel('Iteration')
    plt.ylabel('Value')

    plt.show()

def draw_HITS_iterations():

    auth_list_iteration, hub_list_iteration = graph.get_iteration_auth_hub()
    del auth_list_iteration[0]
    del hub_list_iteration[0]

    length = len(graph.nodes)
    all_auth = [[] for i in range(length)]
    all_hub = [[] for i in range(length)]

    for i in auth_list_iteration:
        for idx, auth in enumerate(i):
            all_auth[idx].append(auth)
    for i in hub_list_iteration:
        for idx, auth in enumerate(i):
            all_hub[idx].append(auth)

    y = [int(i) for i in range(1,len(auth_list_iteration)+1)]

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(15, 5))

    for auth_list in all_auth:
        ax1.plot(y, auth_list)

    for hub_list in all_hub:
        ax2.plot(y, hub_list)

    ax1.title.set_text('Authority on iteration')
    ax1.legend([node.name for node in graph.nodes])
    ax1.set(xlabel='Iteration', ylabel='Value')

    ax2.title.set_text('Hub on iteration')
    ax2.legend([node.name for node in graph.nodes])
    ax2.set(xlabel='Iteration', ylabel='Value')

    plt.show()

if __name__ == '__main__':

    optparser = OptionParser()
    optparser.add_option('-f', '--input_file',
                         dest='input_file',
                         help='CSV filename',
                         default='data/graph_1.txt')
    optparser.add_option('--damping_factor',
                         dest='damping_factor',
                         help='Damping factor (float)',
                         default=0.85,
                         type='float')
    optparser.add_option('--iteration',
                         dest='iteration',
                         help='the number of iterations of the algorithm (int)',
                         default=100,
                         type='int')
    optparser.add_option('--save-iterations',
                         dest='save_iterations',
                         help='output to files in result folder (string)',
                         default='yes',
                         type='string')
    optparser.add_option('--draw-iterations',
                         dest='draw_iterations',
                         help='create a graph for iterations (string)',
                         default='no',
                         type='string')
    optparser.add_option('--draw-graphmat',
                         dest='draw_graphmat',
                         help='create a graph using Matplotlib software (string)',
                         default='no',
                         type='string')
    optparser.add_option('--draw-graphviz',
                         dest='draw_graphviz',
                         help='create a graph using Graphviz software (string)',
                         default='no',
                         type='string')
    optparser.add_option('--graphviz-dot-file',
                         dest='graphviz_dot_file',
                         help='Graphviz DOT file (string)',
                         default='doc/graph_1.gv',
                         type='string')

    (options, args) = optparser.parse_args()

    file_path = options.input_file
    iteration = options.iteration
    damping_factor = options.damping_factor
    save_iterations = options.save_iterations
    draw_iterations = options.draw_iterations
    draw_graphmat = options.draw_graphmat
    draw_graphviz = options.draw_graphviz
    graphviz_dot_file = options.graphviz_dot_file

    result_dir = 'result'
    fname = file_path.split('/')[-1].split('.')[0]

    graph = init_graph(file_path)

    output_HITS(iteration, graph, result_dir, fname, save_iterations)
    output_PageRank(iteration, graph, damping_factor, result_dir, fname, save_iterations)

    if draw_iterations == 'yes':
        import matplotlib.pyplot as plt
        
        draw_PageRank_iterations()
        draw_HITS_iterations()

    if draw_graphmat == 'yes':
        import networkx as nx
        import matplotlib.pyplot as plt

        draw_graph_to_file(file_path, result_dir, fname)

    if draw_graphviz == 'yes':
        import pathlib
        from graphviz import Source

        file = pathlib.Path(graphviz_dot_file)
        s = Source.from_file(file, format = 'png', engine = 'fdp', encoding = 'utf8')
        # print(s.source)
        s.view()