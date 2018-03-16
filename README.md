# Civ 6 Civics, Technologies, and Boosts represented as a Directed Acyclic Graph

## Introduction

Attempt at applying Data Analysis, or Data Science to Sid Meier's Civilization 6's Civics, Technologies, and corresponding boosts. The output is a Directed Acyclic Graph depicting the combined trees.

This project follows a common Data Science Workflow to create a "Data Product":

1. Preparation
2. Analysis
3. Reflection
4. Dissemination

### Preparation

All Data Products serve to answer a question, preferably an interesting one. In Civ 6 the Civics and Technology trees are separate however they are interlinked in some subtle and non-subtle ways. The purpose of the project is to answer the question:

> How are the Civics, Technologies, and general gameplay intertwined?

The Civic and Technology tree data is easily accessible in the GamePlay sqlite database and a set of SQL queries went a long way. Gathering the boosts data was a little trickier. The raw data is in the gameplay db, however it isn't easily usable in the Graph. In the end I extracted the raw data into Microsoft Excel and exported the Boost related nodes (vertexes) and edges as CSV files for addition to the output graph.

The nodes and edges are also colour coded and styled to help you interpret the graph created using the Python NetworkX module. Some nodes and edges were changed (or even deleted) to reduce unnecessary complexity.

Lastly, this my first ever project using Python and the code is rough around the edges, ie. very little error checking, exception handling, nor logging is implemented.

### Analysis

![Full graph of the Civics, Technologies, and Boosts](output/civ6_networkx.png)

Courtesy of NetworkX, the graph (network) properties are:

* Name: Civ 6 R&F Civic, Technology, and Boosts network
* Type: DiGraph
* Number of nodes: 357
* Number of edges: 526
* Average in degree:   1.4734
* Average out degree:   1.4734
* Network density: 0.004

In summary this tells us that we have a sparse network. That is, this is about a far from the common social network data science examples popular on the internet as we can get.

Degree is a measure of how many in and out connections each node has. The assumption here is that the important nodes have more connections. The nodes with high degree as usually known as the Hubs. In this graph the top 10 nodes by degree are:

1. Settle First City (10)
2. Natural History (10)
3. Mining (10)
4. Radio (9)
5. Guilds (8)
6. Humanism (8)
7. Ideology (8)
8. Education (8)
9. Industrialization (8)
10. Flight (8)

Betweenness centrally is good at finding nodes that connect two otherwise disparate parts of a network. That is, highlighting the Brokers. In this graph the top 10 nodes by betweenness centrally are:

1. Flight (0.026)
2. Industrialization (0.025)
3. Scientific Theory (0.022)
4. Radio (0.022)
5. Humanism (0.020)
6. Guilds (0.019)
7. Defensive Tactics (0.019)
8. Banking (0.015)
9. Gunpowder (0.015)
10. Feudalism (0.014)

A very simple graph showing the potential routes to Archery:

![Routes to Archery](output/RouteToArchery.png)

A more complex graph showing the potential routes to Stirrups:

![Routes to Stirrups](output/RouteToStirrups.png)

### Reflection

I didn't find any real surprises in the Hub or Broker nodes. I was however pleasantly surprised with the route(s) to Stirrups. I knew it was broad but seeing it visually was still an interesting experience. Also, as it contains most key civics and many useful technologies it would make sense to look at minimising the costs (and turns) associate with getting Stirrups.

As it stands the graph is a good base to generate routes to other node images, and I look forward to exploring these.

Turning to NetworkX, and the general data science toolset in Python. I can honestly say that I was happy to learn how easy to use they are. And, how much depth there is to the tools. Off course, I am merely scraping the surface and there is loads of complexity under the covers.

### Dissemination

If you are reading this, you have been disseminated to. I doubt this project will feature in any academic publications, but the internet is a large place and you never know.

## Getting Started

Using the code is relatively simple if you have any experience using GitHub and Python. All you need is a python interpreter and a place to download the python scripts to.

The code assumes you are using Python 3.6 and consumes the following additional modules (all installed via Pip):

* graphviz (x.x)
* networkx (2.1)
* pydotplus (2.0.2)

### Project structure and usage guidelines

CreateCiv6NetworkNodesAndEdges uses the GamePlay sqlite database and Microsoft Excel xlsx and csv files in the input folder to create the civ6NodesAndEdges.json file.

All the SQL queries to extract the nodes and edges are in the CreateCiv6NetworkQueries file, and the CreateCiv6NetworkUtilities file has the collection of constants and functions used by the other scripts.

CreateCiv6Network takes the json file as input and does the actual graph creation and general analysis. The graphs are put into the output folder by default

## Contribute

I'm not sure where I want to take this next, and your feedback will help shape the eventual outcome.

Here are some simple things I believe you could do to make this more useful:

* Review the network graph(s) and point out any mistakes.
  * Improving data quality is always beneficial!
* Review the code and "pythonise" it.
  * I am a Python newbie
* Any GraphViz wizards out there can improve the output graphs look and feel.
  * Start with adding a legend, please.
* Share your ideas and thoughts.

In the medium-term the graph has possibilities as a lookup tool. If you turn the nodes into html records you could simulate the tech and civic trees.

Longer-term I am interested in fleshing out the graph to include game events and work on some shortest path analysis. E.g. if you look at the drawing above for the route(s) to Stirrups you clearly see that you need to complete activities in both trees and the boosts to minimise the overall costs. Also, boosts in general function as converters of production into culture or science, so the minimum cost calculation is non-trivial.