#!/usr/bin/env python

## graph 1
## directed graph, represented as a dictionary where key n represents node n
## and key n points to a list with a list of nodes n is connected to

graph_1 = {}
graph_1['2'] = []
graph_1['3'] = ['8','10']
graph_1['5'] = ['11']
graph_1['7'] = ['8','11']
graph_1['8'] = ['9']
graph_1['9'] = []
graph_1['10'] = []
graph_1['11'] = ['2','9','10']

print "graph_1 connections"
for key,value in graph_1.iteritems():
	print "node:",key,"connected to:",value

## graph 2
## undirected graph, represented as a symetric matrix
## create_graph_matrix accepts a list of connection tuples
## and creates a matrix representation n by n matrix
## where n is the number of nodes 

graph_2_connections = [(1,2),(1,5),(2,5),(2,3),(3,4),(4,5),(5,6)]
def create_graph_matrix(connections):
	max_node = max([ max(connection) for connection in connections ])
	graph = [ [ 0 for n in range(max_node) ] for m in  range(max_node) ] 
	
	for connection in connections:
		graph[connection[0]-1][connection[1]-1] = 1
		graph[connection[1]-1][connection[0]-1] = 1

	return graph

graph_2 = create_graph_matrix(graph_2_connections)
print "graph_2 as list of lists", graph_2

for n in range(len(graph_2)):
	print "node:",str(n+1),"connected to:",graph_2[n]
