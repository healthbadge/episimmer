import Graph
import sys

n=int(sys.argv[1])
p=float(sys.argv[2])
graph_obj = Graph.RandomGraph(n,p,False)
graph_obj.write_to_simple_adjacency_list_file()
graph_obj.write_to_simple_edge_list_file()