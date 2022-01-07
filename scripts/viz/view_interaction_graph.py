import argparse
from csv import DictReader

from pyvis.network import Network


def get_interaction_graph_from_file(number_of_agents, interaction_file_path):

    fp = open(interaction_file_path, 'r')
    file_type = interaction_file_path[-3:]

    outpath = interaction_file_path[:-3] + 'html'
    net = Network()
    if (file_type == 'txt'):
        num = int(fp.readline())
        fp.readline()

        ls = list(range(number_of_agents))

        net.add_nodes(ls)

        for i in range(num):
            line = fp.readline()
            line = line[:-1]
            a, b = line.split(':')
            net.add_edge(int(a), int(b))

    elif (file_type == 'csv'):
        csv_dict_reader = DictReader(fp)
        csv_list = list(csv_dict_reader)
        n = len(csv_list)
        ls = list(range(n))
        net.add_nodes(ls)

        for i in range(n):
            info_dict = csv_list[i]
            net.add_edge(int(info_dict['Agent Index']),
                         int(info_dict['Interacting Agent Index']))

    fp.close()
    net.show_buttons(filter_=['physics'])
    net.show(outpath)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Utility function for generating interaction graph',
        usage='% (prog)s filename [options]')

    arg_parser.add_argument('--number', '-n', required=True)
    arg_parser.add_argument('--filename', '-f', required=True)

    args = arg_parser.parse_args()

    get_interaction_graph_from_file(int(args.number), args.filename)
