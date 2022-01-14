import argparse
from csv import DictReader

from episimmer.read_file import ReadConfiguration


def get_value(line):
    if line.endswith('\n'):
        line = line[:-1]
    return line


def get_file_keys(filename):
    if filename.endswith('.txt'):
        f = open(filename, 'r')
        n = int(get_value(f.readline()))
        agent_info_keys = get_value(f.readline())

    elif filename.endswith('.csv'):
        with open(filename, 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            agent_info_keys = ':'.join(csv_dict_reader.fieldnames)

    return agent_info_keys


def write_files_list(filename, type):
    list_filename = None
    if type == 'interactions':
        list_filename = 'interaction_files_list.txt'

    elif type == 'events':
        list_filename = 'event_files_list.txt'

    elif type == 'pinteractions':
        list_filename = 'probabilistic_interaction_files_list.txt'

    f = open(list_filename, 'w')
    f.write('<{0}>'.format(filename))
    f.close()

    return list_filename


def write_config_file(final_dict):
    f = open('config.txt', 'w')
    f.write('Random Seed <{0}>\n\
Number of worlds <{1}>\n\
Number of Days <{2}>\n\
Agent Parameter Keys <{3}>\n\
Agent list filename <{4}>\n\
Interaction Info Keys <{5}>\n\
Interaction Files list filename <{6}>\n\
Probabilistic Interaction Files list filename <{7}>\n\
Location Parameter Keys <{8}>\n\
Location list filename <{9}>\n\
Event Parameter Keys <{10}>\n\
Event Files list filename <{11}>\n\
One Time Event filename <{12}>\n'.format(*final_dict.values()))

    f.close()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Utility functions for generating config file')

    # options
    arg_parser.add_argument('--fromfile',
                            '-ff',
                            dest='config_filename',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--random',
                            '-rs',
                            dest='random_seed',
                            type=int,
                            default=-1,
                            required=False)
    arg_parser.add_argument('--nworlds',
                            '-nw',
                            dest='nworlds',
                            type=int,
                            default=-1,
                            required=False)
    arg_parser.add_argument('--ndays',
                            '-nd',
                            dest='ndays',
                            type=int,
                            default=-1,
                            required=False)
    arg_parser.add_argument('--agents',
                            '-af',
                            dest='agent_file',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--interactions',
                            '-if',
                            dest='interaction_file',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--pinteractions',
                            '-pif',
                            dest='prob_interaction_file',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--locations',
                            '-locf',
                            dest='location_file',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--events',
                            '-ef',
                            dest='event_file',
                            type=str,
                            default='',
                            required=False)
    arg_parser.add_argument('--otevents',
                            '-otf',
                            dest='ot_event_file',
                            type=str,
                            default='',
                            required=False)

    args = arg_parser.parse_args()

    final_dict = {
        'random_seed': '',
        'worlds': '',
        'days': '',
        'agent_keys': '',
        'agent_file': '',
        'interaction_keys': '',
        'interaction_file': '',
        'prob_interaction_file': '',
        'location_keys': '',
        'location_file': '',
        'event_keys': '',
        'event_file': '',
        'one_time_event_file': ''
    }

    if args.config_filename != '':
        config_obj = ReadConfiguration(args.config_filename)

    else:
        config_obj = ReadConfiguration('start_config.txt')

    final_dict[
        'random_seed'] = args.random_seed if args.random_seed != -1 else config_obj.random_seed
    final_dict[
        'worlds'] = args.nworlds if args.nworlds != -1 else config_obj.worlds
    final_dict[
        'days'] = args.ndays if args.ndays != -1 else config_obj.time_steps

    if args.agent_file != '':
        final_dict['agent_keys'] = get_file_keys(args.agent_file)
        final_dict['agent_file'] = args.agent_file

    else:
        final_dict['agent_keys'] = config_obj.agent_info_keys
        final_dict['agent_file'] = config_obj.agents_filename

    if args.interaction_file != '':
        final_dict['interaction_keys'] = get_file_keys(args.interaction_file)
        final_dict['interaction_file'] = write_files_list(
            args.interaction_file, 'interactions')

    else:
        final_dict['interaction_keys'] = config_obj.interaction_info_keys
        final_dict['interaction_file'] = ','.join(
            config_obj.interactions_files_list_list)

    if args.location_file != '':
        final_dict['location_keys'] = get_file_keys(args.location_file)
        final_dict['location_file'] = args.location_file

    else:
        final_dict['location_keys'] = config_obj.location_info_keys
        final_dict['location_file'] = config_obj.locations_filename

    if args.event_file != '':
        final_dict['event_keys'] = get_file_keys(args.event_file)
        final_dict['event_file'] = write_files_list(args.event_file, 'events')

    else:
        final_dict['event_keys'] = config_obj.event_info_keys
        final_dict['event_file'] = ','.join(config_obj.events_files_list_list)

    if args.prob_interaction_file != '':
        final_dict['prob_interaction_file'] = write_files_list(
            args.prob_interaction_file, 'pinteractions')
    else:
        final_dict['prob_interaction_file'] = ','.join(
            config_obj.probabilistic_interactions_files_list_list)

    if args.ot_event_file != '':
        final_dict['one_time_event_file'] = args.ot_event_file
    else:
        config_obj.one_time_event_file

    write_config_file(final_dict)
