import sqlite3
import networkx as nx
import graphviz as gv
import pydotplus as pd
import CreateCiv6NetworkUtilities as u
import CreateCiv6NetworkQueries as q
import os
import csv

# This file is all about creating the nodes/edges we wish to use in the Civ6 Network analysis.

# Fetch all the relevent data from the gameplay database
dbGameplay = sqlite3.connect(u.civ6GameplayDbFilename)

civicNodesData = dbGameplay.execute(q.civicNodesQueryString).fetchall()
civicEdgesData = dbGameplay.execute(q.civicEdgesQueryString).fetchall()
techNodesData = dbGameplay.execute(q.techNodesQueryString).fetchall()
techEdgesData = dbGameplay.execute(q.techEdgesQueryString).fetchall()
districtNodesData = dbGameplay.execute(q.districtNodesQueryString).fetchall()
districtEdgesData = dbGameplay.execute(q.districtEdgesQueryString).fetchall()
wonderNodesData = dbGameplay.execute(q.wonderNodesQueryString).fetchall()
wonderEdgesData = dbGameplay.execute(q.wonderEdgesQueryString).fetchall()
buildingNodesData = dbGameplay.execute(q.buildingNodesQueryString).fetchall()
buildingEdgesData = dbGameplay.execute(q.buildingEdgesQueryString).fetchall()

dbGameplay.close()

# Boost are manually edited in CSV files, load and process them
boostNodesData = []
boostNodesCSVFilename = "{0}\\input\\boost-nodes.csv".format(os.path.dirname(os.path.abspath(__file__)))
with open(boostNodesCSVFilename) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'Node':
            continue
        boostNodesData.append((row[0], row[1], int(row[2]), row[3], row[4], row[5]))
boostEdgesCSVFilename = "{0}\\input\\boost-edges.csv".format(os.path.dirname(os.path.abspath(__file__)))
boostEdgesData = []
with open(boostEdgesCSVFilename) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'FromNode':
            continue
        boostEdgesData.append((row[0], row[1], 'Boost'))

# Merge the raw data into the respective lists
rawNodesDataList = civicNodesData + techNodesData + districtNodesData + wonderNodesData + buildingNodesData + boostNodesData
rawEdgesDataList = civicEdgesData + techEdgesData + districtEdgesData + wonderEdgesData + buildingEdgesData + boostEdgesData

# Clean-up data
# 1. Add missing nodes, especially the "root" node
# 2. Add missing edges, especially from "root" node to Civic and Technology trees
# 3. Remove buildings and corresponding edges to simplify. E.g. not Showing government plaza buildings.
# 4. Replace/Changes edges that confuse things. E.g. You must have campus in order to build a library,
#    even though they both have Writing as the pre-requisite technology
# 5. Convert nodesData from 6-tuple to 2-tuple with the 2nd element being a dictionary of attributes - expected format for networkx
#    Convert edgesData from 3-tuple to 3-tuple with the 3rd element being a dictionary of attributes - expected format for networkx
# 1.
rawNodesDataList.append(('SETTLE_FIRST_CITY', 'Settle First City', 0, 'P', 'Ancient Era', 'None'))
# 2.
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'CIVIC_CODE_OF_LAWS', 'Civic'))
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'TECH_POTTERY', 'Technology'))
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'TECH_ANIMAL_HUSBANDRY', 'Technology'))
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'TECH_MINING', 'Technology'))
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'TECH_SAILING', 'Technology'))
rawEdgesDataList.append(('SETTLE_FIRST_CITY', 'TECH_ASTROLOGY', 'Technology'))
rawEdgesDataList.append(('DISTRICT_ENCAMPMENT', 'BUILDING_STABLE', 'Building'))
# 3. Prepare to remove
nodesToRemove = ['BUILDING_GOV_CONQUEST', 'BUILDING_GOV_TALL', 'BUILDING_GOV_WIDE', 'BUILDING_GOV_CITYSTATES', 'BUILDING_GOV_FAITH',
                 'BUILDING_GOV_SPIES', 'BUILDING_GOV_CULTURE', 'BUILDING_GOV_MILITARY', 'BUILDING_GOV_SCIENCE', 'BUILDING_GURDWARA',
                 'BUILDING_MEETING_HOUSE', 'BUILDING_MOSQUE', 'BUILDING_PAGODA', 'BUILDING_SYNAGOGUE', 'BUILDING_WAT', 'BUILDING_STUPA',
                 'BUILDING_DAR_E_MEHR']
# 4. Prepare to change
edgesToChange = [(('TECH_WRITING','BUILDING_LIBRARY', 'Building'),('DISTRICT_CAMPUS','BUILDING_LIBRARY', 'Building'))
                ,(('CIVIC_GAMES_RECREATION', 'BUILDING_ARENA', 'Building'),('DISTRICT_ENTERTAINMENT_COMPLEX', 'BUILDING_ARENA', 'Building'))
                ,(('TECH_CURRENCY', 'BUILDING_MARKET', 'Building'),('DISTRICT_COMMERCIAL_HUB', 'BUILDING_MARKET', 'Building'))
                ,(('TECH_BRONZE_WORKING', 'BUILDING_BARRACKS', 'Building'),('DISTRICT_ENCAMPMENT', 'BUILDING_BARRACKS', 'Building'))
                ,(('TECH_APPRENTICESHIP', 'BUILDING_WORKSHOP', 'Building'),('DISTRICT_INDUSTRIAL_ZONE', 'BUILDING_WORKSHOP', 'Building'))
                ,(('TECH_ASTROLOGY', 'BUILDING_SHRINE', 'Building'),('DISTRICT_HOLY_SITE', 'BUILDING_SHRINE', 'Building'))
                ,(('CIVIC_DRAMA_POETRY', 'BUILDING_AMPHITHEATER', 'Building'),('DISTRICT_THEATER', 'BUILDING_AMPHITHEATER', 'Building'))
                ,(('TECH_CELESTIAL_NAVIGATION', 'BUILDING_LIGHTHOUSE', 'Building'),('DISTRICT_HARBOR', 'BUILDING_LIGHTHOUSE', 'Building'))
                ,(('CIVIC_NATURAL_HISTORY', 'BUILDING_FERRIS_WHEEL', 'Building'),('DISTRICT_WATER_ENTERTAINMENT_COMPLEX', 'BUILDING_FERRIS_WHEEL', 'Building'))]
# 3, 4 & 5. - Loop through nodes data, amkignthe necessary changes.
nodesDataList = []
for node in rawNodesDataList:
    if node[0] in nodesToRemove:
        # 3. Simply skip copying it the output
        continue
    nodesDataList.append(u.convertNodeDataToNode(node)) # 5.
# 3, 4 & 5. - Loop through edges data, making the necessary changes.
edgesDataList = []
for edge in rawEdgesDataList:
    if edge[0] in nodesToRemove or edge[1] in nodesToRemove:
        # 3. Don't keep any edges that have nodes in the nodes to remove list
        continue
    # Change out the edges to change
    skipEdge = False
    # This isn't very efficient, but it is simple and works.
    for item in edgesToChange:
        if edge == item[0]:
            # 4. If we get here we've found an edge we wish to change, so change it
            edgesDataList.append(u.convertEdgeDataToEdge(item[1])) # 5.
            skipEdge = True
            continue
    if skipEdge:
        continue
    else:
        edgesDataList.append(u.convertEdgeDataToEdge(edge)) #5.

# Convert to final nodes and edges
# 1. Get the categorised lists to apply conditional formatting to nodes and edges
# 2. Apply attributes based on category to nodes and edges
# 3. Make style for edges between boosts and associate civic or technologies dashed
# 1.
civicNodes = list(x for x in nodesDataList if x[1]['category'] == 'Civic')
civicEdges = list(x for x in edgesDataList if x[2]['category'] == 'Civic')
techNodes =  list(x for x in nodesDataList if x[1]['category'] == 'Technology')
techEdges = list(x for x in edgesDataList if x[2]['category'] == 'Technology')
districtNodes = list(x for x in nodesDataList if x[1]['category'] == 'District')
districtEdges = list(x for x in edgesDataList if x[2]['category'] == 'District')
wonderNodes = list(x for x in nodesDataList if x[1]['category'] == 'Wonder')
wonderEdges = list(x for x in edgesDataList if x[2]['category'] == 'Wonder')
buildingNodes = list(x for x in nodesDataList if x[1]['category'] == 'Building')
buildingEdges = list(x for x in edgesDataList if x[2]['category'] == 'Building')
unitNodes = list(x for x in nodesDataList if x[1]['category'] == 'Unit')
unitEdges = list(x for x in edgesDataList if x[2]['category'] == 'Unit')
boostNodes = list(x for x in nodesDataList if x[1]['category'] == 'Boost')
boostEdges = list(x for x in edgesDataList if x[2]['category'] == 'Boost')
noneNodes = list(x for x in nodesDataList if x[1]['category'] == 'None')
noneEdges = list(x for x in edgesDataList if x[2]['category'] == 'None')
# 2. for nodes
nodes = []
for node in noneNodes:
    nodes.append((node[0], {**(node[1]), **u.noneNodeDefaults}))
for node in boostNodes:
    nodes.append((node[0], {**(node[1]), **u.boostNodeDefaults}))
for node in civicNodes:
    nodes.append((node[0], {**(node[1]), **u.civicNodeDefaults}))
for node in techNodes:
    nodes.append((node[0], {**(node[1]), **u.techNodeDefaults}))
for node in districtNodes:
    nodes.append((node[0], {**(node[1]), **u.districtNodeDefaults}))
for node in wonderNodes:
    nodes.append((node[0], {**(node[1]), **u.wonderNodeDefaults}))
for node in buildingNodes:
    nodes.append((node[0], {**(node[1]), **u.buildingNodeDefaults}))
for node in unitNodes:
    nodes.append((node[0], {**(node[1]), **u.unitNodeDefaults}))
# 2. for edges
edges = []
for edge in noneEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.noneEdgeDefaults}))
for edge in boostEdges:
    lineStyle = 'solid'
    if edge[0].startswith('BOOST_') and (edge[1].startswith('CIVIC_') or edge[1].startswith('TECH_')):
        # 4. Make style for edges between boosts and associate civic or technologies dashed
        lineStyle = 'dashed'
    edges.append((edge[0], edge[1], {**edge[2], **u.boostEdgeDefaults, **{ 'style':lineStyle}}))
for edge in civicEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.civicEdgeDefaults}))
for edge in techEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.techEdgeDefaults}))
for edge in districtEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.districtEdgeDefaults}))
for edge in wonderEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.wonderEdgeDefaults}))
for edge in buildingEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.buildingEdgeDefaults}))
for edge in unitEdges:
    edges.append((edge[0], edge[1], {**edge[2], **u.unitEdgeDefaults}))

# All the data created, save it to disk so we can start playing with graphs and "interesing" stuff
u.saveCiv6NetworkData(nodes, edges, r'civ6NodesAndEdges.json')
