import networkx as nx
import pandas as pd
from LearningMethods.taxtreeCreate import create_tax_tree
from ete3 import Tree, TreeStyle, NodeStyle


def name_to_newick(tup):
    return str(tup).replace(", ", "|").replace("(", "<")\
        .replace(")", ">").replace("'", "").replace(",", "")

def newick_to_name(string):
    return tuple(string.strip("<>").split("|"))

def tree_to_newick_recursion(g, root=("anaerobe",)):
    if root is None:
        roots = list(filter(lambda p: p[1] == 0, g.in_degree()))
        assert 1 == len(roots)
        root = roots[0][0]
    subgs = []
    for child in g[root]:
        if len(child) > len(root) or root == ("anaerobe",):
            if len(g[child]) > 1:
                subgs.append(tree_to_newick_recursion(g, root=child))
            else:
                subgs.append(name_to_newick(child))
    return "(" + ','.join(subgs) + ")" + name_to_newick(root)

def tree_to_newick(s):
    graph = create_tax_tree(s)
    newick = tree_to_newick_recursion(graph) + ";"
    return newick, graph

def get_tree_shape(newick, graph, lower_threshold, higher_threshold):
    t = Tree(newick, format=8)
    for n in t.traverse():
        nstyle = NodeStyle()
        nstyle["fgcolor"] = "yellow"
        name = newick_to_name(n.name)
        if name != '':
            if graph.nodes[name]["val"] > higher_threshold:
                nstyle["fgcolor"] = "green"
            elif graph.nodes[name]["val"] < lower_threshold:
                nstyle["fgcolor"] = "red"
        nstyle["size"] = 5
        n.set_style(nstyle)
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.min_leaf_separation = 0.5
    ts.mode = "c"
    ts.root_opening_factor = 0.75
    return t, ts

def draw_tree(series, threshold=1.0, folder="static", name="phylotree"):
    if type(threshold) == tuple:
        lower_threshold, higher_threshold = threshold
    else:
        lower_threshold, higher_threshold = -threshold, threshold
    newick, graph = tree_to_newick(series)
    t, ts = get_tree_shape(newick, graph, lower_threshold, higher_threshold)
    t.render(f"{folder}/{name}.svg", tree_style=ts)
    return t, ts
    #t.show(tree_style=ts)

if __name__=="__main__":
    df = pd.read_csv("test_set_Cirrhosis_microbiome.csv", index_col=0)
    s = df.iloc[0]
    t, ts = draw_tree(s, (0.9, 1.1))
    t.show(tree_style=ts)

