import os
import networkx as nx
import graphviz as gv
import pydotplus as pd
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

pdGraph = pd.Dot(graph_type='digraph', rankdir='LR', newrank=True)
civicGraph = pd.Subgraph('cluster_civic', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.0)
#restGraph = pd.Subgraph('cluster_rest', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.0)
techGraph = pd.Subgraph('cluster_tech', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.0)

for node in nodes:
    if node[1]['category'] == 'Civic':
        civicGraph.add_node(pd.Node(name=node[0], **node[1]))
    elif node[1]['category'] == 'Technology':
        techGraph.add_node(pd.Node(name=node[0], **node[1]))
    else:
        if str(node[0]).startswith('BOOST_CIVIC_'):
            civicGraph.add_node(pd.Node(name=node[0], **node[1]))
        elif str(node[0]).startswith('BOOST_TECH_'):
            techGraph.add_node(pd.Node(name=node[0], **node[1]))
        else:
            pdGraph.add_node(pd.Node(name=node[0], **node[1]))

# For the drawing purposes we can ignore the complexity of worrying which edges are where?
for edge in edges:
    pdGraph.add_edge(pd.Edge(src=edge[0], dst=edge[1], **edge[2]))

pdGraph.add_subgraph(civicGraph)
#pdGraph.add_subgraph(restGraph)
pdGraph.add_subgraph(techGraph)

# # try to generate a pretty picture using pydotplus and graphviz clusters...
# pdGraph = pd.Dot(graph_type='digraph', rankdir='LR', newrank=True)
# # split by age
# ancientEraGraph = pd.Subgraph('cluster_ancient', label='Ancient Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# classicalEraGraph = pd.Subgraph('cluster_classical', label='Classical Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# medievalEraGraph = pd.Subgraph('cluster_medieval', label='Medieval Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# renaissanceEraGraph = pd.Subgraph('cluster_renaissance', label='Renaissance Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# industrialEraGraph = pd.Subgraph('cluster_industrial', label='Industrial Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# modernEraGraph = pd.Subgraph('cluster_modern', label='Modern Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# atomicEraGraph = pd.Subgraph('cluster_atomic', label='Atomic Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)
# infoEraGraph = pd.Subgraph('cluster_info', label='Information Era', pencolor="#D3D3D3", style='dashed', fontsize=24, penwidth=0.5)

# for node in nodes:
#     if node[1]['era'] == 'Ancient':
#         ancientEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Classical':
#         classicalEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Medieval':
#         medievalEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Renaissance':
#         renaissanceEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Industrial':
#         industrialEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Modern':
#         modernEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Atomic':
#         atomicEraGraph.add_node(pd.Node(name=node[0], **node[1]))
#     if node[1]['era'] == 'Information':
#         infoEraGraph.add_node(pd.Node(name=node[0], **node[1]))

# # For the drawing purposes we can ignore the complexity of worrying which edges are where?
# for edge in edges:
#     pdGraph.add_edge(pd.Edge(src=edge[0], dst=edge[1], **edge[2]))

# pdGraph.add_subgraph(ancientEraGraph)
# pdGraph.add_subgraph(classicalEraGraph)
# pdGraph.add_subgraph(medievalEraGraph)
# pdGraph.add_subgraph(renaissanceEraGraph)
# pdGraph.add_subgraph(industrialEraGraph)
# pdGraph.add_subgraph(modernEraGraph)
# pdGraph.add_subgraph(atomicEraGraph)
# pdGraph.add_subgraph(infoEraGraph)

# pdGraph.set('rank', "same; cluster_ancient; cluster_classical; cluster_medieval")

s = gv.Source(pdGraph.to_string(), "{0}\\output\\civ6_pydot1".format(os.path.dirname(os.path.abspath(__file__))), format='svg')
s.view()

#print(type(pdGraph))
#print(pdGraph.to_string())