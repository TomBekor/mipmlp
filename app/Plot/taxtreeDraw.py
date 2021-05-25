from LearningMethods.textreeCreate import create_tax_tree
import networkx as nx
import pickle
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


def draw_tree(graph, threshold=0.0):
    if type(threshold) == tuple:
        lower_threshold, higher_threshold = threshold
    else:
        lower_threshold, higher_threshold = -threshold, threshold
    labelg = {}
    labelr = {}
    colormap = []
    sizemap = []
    for node in graph:
        if node[0] == "base":
            colormap.append("white")
            sizemap.append(0)
        else:
            if node[1] < lower_threshold:
                colormap.append("red")
                labelr[node] = node[0][-1]
            elif node[1] > higher_threshold:
                colormap.append("green")
                labelg[node] = node[0][-1]
            else:
                colormap.append("yellow")
            sizemap.append(node[1] / 1000 + 5)
    # drawing the graph
    pos = graphviz_layout(graph, prog="twopi", root="base")
    #pos = nx.spring_layout(graph)
    lpos = {}
    for key, loc in pos.items():
        lpos[key] = (loc[0], loc[1] + 0.02)
    nx.draw(graph, pos, node_size=sizemap, node_color=colormap, width=0.3)
    nx.nx.draw_networkx_labels(graph, lpos, labelr, font_size=7, font_color="red")
    nx.nx.draw_networkx_labels(graph, lpos, labelg, font_size=7, font_color="green")
    plt.draw()
    plt.savefig("taxtree.png")

if __name__ == "__main__":
    with open("series.p", "rb") as f:
        draw_tree(create_tax_tree(pickle.load(f)), 25)
