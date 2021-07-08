import sys
sys.path.insert(1, '../../src/')

from pyvis.network import Network
import argparse
from Utility import module_from_file

def get_model(filename):
    UserModel = module_from_file("Generate_model", filename)
    model = UserModel.UserModel()
    return model

def get_model_graph(filename):

    model = get_model(filename)
    outpath = filename[:-2]+"html"
    net = Network(directed=True)
    states = model.individual_state_types
    infected_states = model.infected_states
    for i,state in enumerate(states):
        if(state in infected_states):
            net.add_node(i, label=state, shape='box', color = '#fc9283', borderWidth=30, borderWidthSelected=30)
        else:
            net.add_node(i, label=state, shape='box', color = '#99bdf7', borderWidth=30, borderWidthSelected=30)

    transitions = model.transmission_prob
    for i,state_i in enumerate(states):
        for j,state_j in enumerate(states):
            if(transitions[state_i][state_j].args!=(0,)):
                str1 = '<function StochasticModel.'
                str2 = str(transitions[state_i][state_j].func.__func__)[len(str1):]
                func_name = str2.split(' ')[0]
                if(func_name=="full_p_infection"):
                    net.add_edge(i,j,color='#fc9283')
                else:
                    net.add_edge(i,j,color='#99bdf7')


    net.show(outpath)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Utility function for generating disease model graph", usage='% (prog)s filename [options]')

    arg_parser.add_argument("--filename", "-f", required = True)

    args = arg_parser.parse_args()

    get_model_graph(args.filename)
