from pyvis.network import Network
import argparse
import webbrowser
import os
import os.path as osp
import time


def get_interaction_graph_from_file(number_of_agents, interaction_file_path):

    fp = open(interaction_file_path,'r')
    file_type = interaction_file_path[-3:]

    outpath = 'dynamic_graph.html'
    x = [i for i in range(number_of_agents//10)]*(number_of_agents//10)
    y = [i for i in range(number_of_agents//10)]*(number_of_agents//10)
    # net = Network(layout=True)
    net = Network()
    if(file_type=='txt'):
        num = int(fp.readline())
        fp.readline()

        ls = list(range(number_of_agents))

        net.add_nodes(ls, x=x, y=y)
        # for i in ls:
        #     net.add_node(i, x = x[i], level = i%(number_of_agents//10))

        for i in range(num):
            line = fp.readline()
            line = line[:-1]
            a,b = line.split(':')
            net.add_edge(int(a),int(b))

    elif(file_type=='csv'):
        csv_dict_reader=DictReader(fp)
        csv_list=list(csv_dict_reader)
        n=len(csv_list)
        ls = list(range(n))
        net.add_nodes(ls,x=x,y=y)

        for i in range(n):
            info_dict=csv_list[i]
            net.add_edge(int(info_dict['Agent Index']),int(info_dict['Interacting Agent Index']))

    fp.close()

    # net.toggle_physics(False)
    # net.toggle_stabilization(False)
    net.show(outpath)
    return outpath

def dynamic_graph(number_of_agents, list_interaction_file_path):
    x = 3
    while(x):
        x-=1
        for interaction_file_path in list_interaction_file_path:
            path = get_interaction_graph_from_file(number_of_agents, interaction_file_path)
            filename = 'file:'+os.sep+os.sep+osp.join(os.getcwd(),path)
            webbrowser.open(filename, new=0)
            time.sleep(1)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Utility function for generating interaction graph", usage='% (prog)s filename [options]')

    arg_parser.add_argument("--number", "-n", dest = "number", required = True)

    args = arg_parser.parse_args()
    dynamic_graph(int(args.number), ["interactions_list1.txt","interactions_list2.txt","interactions_list3.txt"]) # List will be changed to interaction_list_file / list of lists
