# Variables and utilities used to create the civ6 network of interest
import os
import sqlite3
import pydotplus as pd
import json

# Paths and filenames
scriptFolder = os.path.dirname(os.path.abspath(__file__))
civ6LocalizationDbFilename = "{0}\\input\\DebugLocalization.sqlite".format(scriptFolder)
civ6GameplayDbFilename = "{0}\\input\\DebugGameplay.sqlite".format(scriptFolder)

# Setup some defaults and helpers used frequently
colourCulture = '#E800E8'
colourScience = '#21BFF7'
colourProduction = '#C78733'
colourDistrict = '#C78733'
colourWonder = '#FFCC00'
colourBoost = '#9EADBF'

civicNodeDefaults = { 'color': colourCulture, 'style':'rounded', 'shape':'box' }
civicEdgeDefaults = { 'color': colourCulture }
techNodeDefaults = { 'color': colourScience, 'style':'rounded', 'shape':'box' }
techEdgeDefaults = {'color' : colourScience }
districtNodeDefaults = { 'color': colourDistrict, 'style':'rounded', 'shape':'box' }
districtEdgeDefaults = {'color' : colourDistrict }
wonderNodeDefaults = { 'color': colourWonder, 'style':'rounded', 'shape':'box' }
wonderEdgeDefaults = {'color' : colourWonder }
buildingNodeDefaults = { 'color': colourProduction, 'style':'rounded', 'shape':'box' }
buildingEdgeDefaults = {'color' : colourProduction }
unitNodeDefaults = { 'color': colourProduction, 'style':'rounded', 'shape':'box' }
unitEdgeDefaults = {'color' : colourProduction }
boostNodeDefaults = { 'color': colourBoost, 'style':'rounded', 'shape':'box' }
boostEdgeDefaults = {'color' : colourBoost }
noneNodeDefaults = { 'color': 'Black', 'style':'rounded', 'shape':'box' }
noneEdgeDefaults = {'color' : 'Black' }


# helper function to format node labels
def makeLabel(text, cost, costType):
    return "{0}\n{1}{2}".format(text, cost, costType) if cost != 0 else text

# helper function to lookup the friendly name of the "node"
def lookupFriendlyName(name):
    try:
        result = (next(x for x in tags if x[0] == name)[1])
        return result
    except StopIteration:
        return name

# convert tuples returned from database into tuple of node and associated dictionary of node attributes
nKeys = ('label', 'baseCost', 'costType', 'era', 'category')
def convertNodeDataToNode(node):
    nValues = (makeLabel(lookupFriendlyName(node[1]), node[2], node[3]),    # label
               node[2],                                                     # baseCost
               node[3],                                                     # costType
               lookupFriendlyName(node[4]),                                 # era
               node[5])                                                     # category
    return (node[0], dict(zip(nKeys, nValues)))

# convert tuples returned from database into tuple of edge and associated dictionary of edge attribute
def convertEdgeDataToEdge(edge):
    return (edge[0], edge[1], {'category': edge[2]})

# convert nodes and edges to a dict, and then save as json file
def saveCiv6NetworkData(nodes, edges, filename):
    civ6NodesAndEdges = {'nodes': nodes, 'edges': edges}
    # print(len(civ6NodesAndEdges['nodes']), civ6NodesAndEdges['nodes'])
    # print(len(civ6NodesAndEdges['edges']), civ6NodesAndEdges['edges'])
    fullpathname = "{0}\\{1}".format(os.path.dirname(os.path.abspath(__file__)), filename)
    json.dump(civ6NodesAndEdges, open(fullpathname, 'w'), indent=2)

# open json file, and then return the nodes and edges generated previously
def openCiv6NetworkData(filename):
    fullpathname = "{0}\\{1}".format(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(fullpathname) as f:
        civ6NodesAndEdges = json.load(f)
    return civ6NodesAndEdges['nodes'], civ6NodesAndEdges['edges']

# Fetch all the English descriptions, and add some apparently missing
dbLocalization = sqlite3.connect(civ6LocalizationDbFilename)
tags = dbLocalization.execute(r"SELECT Tag, Text FROM EnglishText").fetchall()
dbLocalization.close()
tags.append(('LOC_DISTRICT_IKANDA_NAME', 'Ikanda'))
tags.append(('LOC_DISTRICT_SEOWON_NAME', 'Seowon'))
tags.append(('LOC_DISTRICT_GOVERNMENT_NAME', 'Government'))
tags.append(('LOC_DISTRICT_WATER_ENTERTAINMENT_COMPLEX_NAME', 'Waterpark'))
tags.append(('LOC_DISTRICT_WATER_STREET_CARNIVAL_NAME', 'Street Carnival'))
tags.append(('LOC_BUILDING_ORDU_NAME', 'Ordu'))
tags.append(('LOC_BUILDING_TSIKHE_NAME', 'Tsike'))
tags.append(('LOC_BUILDING_FERRIS_WHEEL_NAME', 'Ferris Wheel'))
tags.append(('LOC_BUILDING_AQUARIUM_NAME', 'Aquarium'))
tags.append(('LOC_BUILDING_AQUATICS_CENTER_NAME', 'Aquatics Center'))
tags.append(('LOC_BUILDING_GOV_TALL_NAME', 'Gov Tall?'))
tags.append(('LOC_BUILDING_GOV_WIDE_NAME', 'Gov Wide?'))
tags.append(('LOC_BUILDING_GOV_CONQUEST_NAME', 'Gov Conquest?'))
tags.append(('LOC_BUILDING_GOV_CITYSTATES_NAME', 'Gov CityStates?'))
tags.append(('LOC_BUILDING_GOV_SPIES_NAME', 'Gov Spies?'))
tags.append(('LOC_BUILDING_GOV_FAITH_NAME', 'Gov Faith?'))
tags.append(('LOC_BUILDING_GOV_MILITARY_NAME', 'Gov Military?'))
tags.append(('LOC_BUILDING_GOV_CULTURE_NAME', 'Gov Culture?'))
tags.append(('LOC_BUILDING_GOV_SCIENCE_NAME', 'Gov Science'))
tags.append(('LOC_BUILDING_FOOD_MARKET_NAME', 'Food Market'))
tags.append(('LOC_BUILDING_SHOPPING_MALL_NAME', 'Shopping Mall'))
tags.append(('LOC_BUILDING_TEMPLE_ARTEMIS_NAME', 'Artemis Temple'))
tags.append(('LOC_BUILDING_KILWA_KISIWANI_NAME', 'Kilwa Kisiwani'))
tags.append(('LOC_BUILDING_KOTOKU_IN_NAME', 'Kotoku In'))
tags.append(('LOC_BUILDING_CASA_DE_CONTRATACION_NAME', 'Casa de Contracion'))
tags.append(('LOC_BUILDING_ST_BASILS_CATHEDRAL_NAME', 'St Basils Catherdral'))
tags.append(('LOC_BUILDING_TAJ_MAHAL_NAME', 'Taj Mahal'))
tags.append(('LOC_BUILDING_STATUE_LIBERTY_NAME', 'Statue of Liberty'))
tags.append(('LOC_BUILDING_AMUNDSEN_SCOTT_RESEARCH_STATION_NAME', 'Amunden Scott Research Station'))
tags.append(('LOC_BUILDING_PRASAT_NAME', 'Prasat'))
tags.append(('LOC_BUILDING_ANGKOR_WAT_NAME', 'Angkor Wat'))
tags.append(('LOC_BUILDING_SUKIENNICE_NAME', 'Sukiennice'))
tags.append(('LOC_BUILDING_JEBEL_BARKAL_NAME', 'Jebel Barkal'))
tags.append(('LOC_BUILDING_BASILIKOI_PAIDES_NAME', 'Basilikoi Paides'))
tags.append(('LOC_BUILDING_APADANA_NAME', 'Apadana'))
tags.append(('LOC_BUILDING_HALICARNASSUS_MAUSOLEUM_NAME', 'Halicarnassus Mausoleum'))
tags.append(('ERA_ANCIENT', 'Ancient'))
tags.append(('ERA_CLASSICAL', 'Classical'))
tags.append(('ERA_MEDIEVAL', 'Medieval'))
tags.append(('ERA_RENAISSANCE', 'Renaissance'))
tags.append(('ERA_INDUSTRIAL', 'Industrial'))
tags.append(('ERA_MODERN', 'Modern'))
tags.append(('ERA_ATOMIC', 'Atomic'))
tags.append(('ERA_INFORMATION', 'Information'))
tags.append(('BUILDING_WORSHIP_PLACE', 'Place of Worship'))