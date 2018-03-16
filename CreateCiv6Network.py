import os
import networkx as nx
import graphviz as gv
import CreateCiv6NetworkUtilities as u
from operator import itemgetter

# Helper function to draw the graph to file
def drawGraph(G, filename):
    fullpathname = "{0}\\output\\{1}".format(os.path.dirname(os.path.abspath(__file__)), filename)
    pos = nx.nx_pydot.to_pydot(G)
    pos.set_graph_defaults(rankdir='LR')
    s = gv.Source(pos, filename=fullpathname, format='svg')
    s.view()

# Load the nodes and edges already generated using the CreateCiv6NetworkAndEdges.py scipt
nodes, edges = u.openCiv6NetworkData(r'civ6NodesAndEdges.json')

# create the networkx Directional Graph for analysis
G = nx.DiGraph(name='Civ 6 R&F Civic, Technology, and Boosts network', rankdir='LR')
G.add_nodes_from(nodes)
G.add_edges_from(edges)
# Uncomment drawGraph to greate the networkx graph, alternatively simply open civ6_networkx1.svg
drawGraph(G, r'civ6_networkx')

# Summary information for the graph.
print(nx.info(G))
print("Network density:", nx.density(G), '\n')

# A node’s degree is the sum of its edges. I.e. how many connects to and from that node
degreeDict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degreeDict, 'degree')
sortedDegree = sorted(degreeDict.items(), key=itemgetter(1), reverse=True)
print("Top 15 nodes by degree:")
for d in sortedDegree[:15]:
    print(G.node[d[0]]['label'].split('\n')[0], d[1])

# Betweenness centrality, which is also expressed on a scale of 0 to 1, is fairly good at finding nodes that connect two otherwise disparate parts of a network. If you’re the only thing connecting two clusters, every communication between those clusters has to pass through you. In contrast to a hub, this sort of node is often referred to as a broker.
betweennessDict = nx.betweenness_centrality(G)
nx.set_node_attributes(G, betweennessDict, 'betweenness')
sortedBetweenness = sorted(betweennessDict.items(), key=itemgetter(1), reverse=True)
print("\nTop 15 nodes by betweenness centrally:")
for b in sortedBetweenness[:15]:
   print(G.node[b[0]]['label'].split('\n')[0], b[1])

def createRoutesToGraph(G, node):
    nodes = nx.single_target_shortest_path(G, node).keys()
    return G.subgraph(nodes)

rtG =createRoutesToGraph(G, 'TECH_ARCHERY')
drawGraph(rtG, 'RouteToArchery')
rtG = createRoutesToGraph(G, 'TECH_STIRRUPS')
drawGraph(rtG, 'RouteToStirrups')
rtG = createRoutesToGraph(G, 'CIVIC_POLITICAL_PHILOSOPHY')
drawGraph(rtG, 'RouteToPoliticalPhilosophy')
rtG = createRoutesToGraph(G, 'TECH_MACHINERY')
drawGraph(rtG, 'RouteToMachinery')

# # # Eigenvector centrality cares if you are a hub, but it also cares how many hubs you are connected to. It’s calculated as a value from 0 to 1: the closer to one, the greater the centrality. Eigenvector centrality is useful for understanding which nodes can get information to many other nodes quickly. If you know a lot of well-connected people, you could spread a message very efficiently.
# # eigenvectorDict = nx.eigenvector_centrality(G, max_iter=100_000)
# # nx.set_node_attributes(G, eigenvectorDict, 'eigenvector')
# # sortedEigenvector = sorted(eigenvectorDict.items(), key=itemgetter(1), reverse=True)
# # print("\nTop 15 nodes by betweenness eigenvector:")
# # for b in sortedEigenvector[:15]:
# #    print(G.node[b[0]]['label'].split('\n')[0], b[1])

# # # First get the top 20 nodes by betweenness as a list
# # topBetweenness = sortedBetweenness[:20]
# # # Then find and print their degree
# # print('\n')
# # for tb in topBetweenness: # Loop through top_betweenness
# #     degree = degreeDict[tb[0]]
# #     print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)

# # # https://programminghistorian.org/lessons/exploring-and-analyzing-network-data-with-python

# # for n in G.nodes():
# #     print(n, G.node[n]['era'])
# #print(G.node['SETTLE_FIRST_CITY'])

# # Get and analyse path to CIVIC_POLITICAL_PHILOSOPHY (Polical Philosophy)
# # CIVIC_POLITICAL_PHILOSOPHY
# # TECH_MACHINERY
# # TECH_STIRRUPS
# paths = nx.algorithms.all_simple_paths(G, 'SETTLE_FIRST_CITY', 'CIVIC_POLITICAL_PHILOSOPHY')
# for p in paths:
#    print(p)

# pathsToStirrups = [['SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'CIVIC_CRAFTSMANSHIP', 'CIVIC_STATE_WORKFORCE', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'CIVIC_CRAFTSMANSHIP', 'CIVIC_STATE_WORKFORCE', 'CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'CIVIC_FOREIGN_TRADE', 'CIVIC_EARLY_EMPIRE', 'CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_ANIMAL_HUSBANDRY', 'TECH_ARCHERY', 'TECH_HORSEBACK_RIDING', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_ANIMAL_HUSBANDRY', 'TECH_ARCHERY', 'TECH_HORSEBACK_RIDING', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_ANIMAL_HUSBANDRY', 'BOOST_TECH_HORSEBACK_RIDING', 'TECH_HORSEBACK_RIDING', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_ANIMAL_HUSBANDRY', 'BOOST_TECH_HORSEBACK_RIDING', 'TECH_HORSEBACK_RIDING', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_MINING', 'TECH_MASONRY', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_MINING', 'TECH_THE_WHEEL', 'BUILDING_WATER_MILL', 'BOOST_TECH_CONSTRUCTION', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_MINING', 'BOOST_TECH_MASONRY', 'TECH_MASONRY', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'TECH_MINING', 'BOOST_TECH_THE_WHEEL', 'TECH_THE_WHEEL', 'BUILDING_WATER_MILL', 'BOOST_TECH_CONSTRUCTION', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'UNIT_SCOUT', 'BOOST_CIVIC_FOREIGN_TRADE', 'CIVIC_FOREIGN_TRADE', 'CIVIC_EARLY_EMPIRE', 'CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'UNIT_SCOUT', 'BOOST_CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'UNIT_SLINGER', 'BOOST_TECH_ARCHERY', 'TECH_ARCHERY', 'TECH_HORSEBACK_RIDING', 'TECH_CONSTRUCTION', 'BOOST_CIVIC_GAMES_RECREATION', 'CIVIC_GAMES_RECREATION', 'CIVIC_DEFENSIVE_TACTICS', 'CIVIC_FEUDALISM', 'BOOST_TECH_STIRRUPS', 'TECH_STIRRUPS']
# ,['SETTLE_FIRST_CITY', 'UNIT_SLINGER', 'BOOST_TECH_ARCHERY', 'TECH_ARCHERY', 'TECH_HORSEBACK_RIDING', 'TECH_STIRRUPS']]

# pathsToPoliticalPhilospohy = [['SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'CIVIC_CRAFTSMANSHIP', 'CIVIC_STATE_WORKFORCE', 'CIVIC_POLITICAL_PHILOSOPHY']
# ,['SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'CIVIC_FOREIGN_TRADE', 'CIVIC_EARLY_EMPIRE', 'CIVIC_POLITICAL_PHILOSOPHY']
# ,['SETTLE_FIRST_CITY', 'UNIT_SCOUT', 'BOOST_CIVIC_FOREIGN_TRADE', 'CIVIC_FOREIGN_TRADE', 'CIVIC_EARLY_EMPIRE', 'CIVIC_POLITICAL_PHILOSOPHY']
# ,['SETTLE_FIRST_CITY', 'UNIT_SCOUT', 'BOOST_CIVIC_POLITICAL_PHILOSOPHY', 'CIVIC_POLITICAL_PHILOSOPHY']]

# #print(pathsToStirrups)

# from itertools import chain

# def containsBoost(nodeList):
#     result = False
#     for node in nodeList:
#         if node.startswith('BOOST'):
#             result = True
#             break
#     return result

# requiredPaths = []
# optionalPaths = []
# for nodeList in pathsToPoliticalPhilospohy:
#     if containsBoost(nodeList):
#         optionalPaths.append(nodeList)
#     else:
#         requiredPaths.append(nodeList)

# requiredNodes = list(set(chain(*requiredPaths)))

# #print(requiredPaths)
# #print(optionalPaths)
# #print(requiredNodes)

# ## try a completely different way
# #n = G.nodes(id='TECH_ARCHERY')
# #print(n)
# for p in G.predecessors('TECH_ARCHERY'):
#     print(p)

# #print(nx.algorithms.is_directed_acyclic_graph(G))
# #print(nx.algorithms.ancestors(G, 'TECH_ARCHERY'))
# SG = nx.topological_sort(G)

# longestPath = nx.dag_longest_path(G)
# print(longestPath)

# def createSubgraph(G, node):
#     nodes = nx.single_source_shortest_path(G,node).keys()
#     return G.subgraph(nodes)

