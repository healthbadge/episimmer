import sys
import Engine
import ReadFile

config_filename=sys.argv[1]
graph_filename=sys.argv[2]
config_obj=ReadFile.ReadConfiguration(config_filename)
graph_obj=ReadFile.ReadSimpleGraph('Simple Adjacency List',graph_filename)
#graph_obj=ReadFile.ReadSimpleGraph('Simple Edge List',graph_filename)
Engine.worlds(config_obj,graph_obj)