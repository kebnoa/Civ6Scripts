import os
import networkx as nx
import graphviz as gv
#import pydotplus as pd
import CreateCiv6NetworkUtilities as u

# Helper function to draw the graph to file
def drawGraph(G, filename):
    fullpathname = "{0}\\output\\{1}".format(os.path.dirname(os.path.abspath(__file__)), filename)
    pos = nx.nx_pydot.to_pydot(G)
    pos.set_graph_defaults(rankdir='LR')
#    print(pos.to_string())  # Uncomment to see the dot file created for debugging
    s = gv.Source(pos, filename=fullpathname, format='svg')
    s.view()

# Load the nodes and edges already generated using the CreateCiv6NetworkAndEdges.py scipt
nodes, edges = u.openCiv6NetworkData(r'civ6NodesAndEdges.json')

# create the networkx Directional Graph for analysis
G = nx.DiGraph(rankdir='LR')
G.add_nodes_from(nodes)
G.add_edges_from(edges)
# # print(nx.info(G))
drawGraph(G, r'civ6_networkx1')