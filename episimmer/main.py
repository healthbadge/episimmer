import os
import os.path as osp

from episimmer.read_file import ReadConfiguration, ReadVDConfiguration
from episimmer.utils.arg_parser import parse_args
from episimmer.utils.module_handling import module_from_file
from episimmer.utils.statistics import write_stats
from episimmer.vulnerability_detection.vd import VD
from episimmer.world import World


def get_model(example_path):
    UserModel = module_from_file('Generate_model',
                                 osp.join(example_path, 'UserModel.py'))
    model = UserModel.UserModel()
    return model


def get_policy(example_path):
    Generate_policy = module_from_file(
        'Generate_policy', osp.join(example_path, 'Generate_policy.py'))
    policy_list, event_restriction_fn = Generate_policy.generate_policy()
    return policy_list, event_restriction_fn


def get_config_path(path, filename):
    config_filepath = osp.join(path, filename)
    return config_filepath


@write_stats('stats.pickle', 'stats.txt')
def main():
    args = parse_args()

    example_path = args.example_path
    vuldetect = args.vuldetect
    config_filename = get_config_path(example_path, 'config.txt')

    config_obj = ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
        events_FilesList_filename, locations_filename, one_time_event_file, probabilistic_interactions_FilesList_filename = config_obj.get_file_paths(example_path)
    interactions_files_list, events_files_list, probabilistic_interactions_files_list = config_obj.get_file_names_list(
        example_path, interactions_FilesList_filename,
        events_FilesList_filename,
        probabilistic_interactions_FilesList_filename)

    # User Model and Policy
    model = get_model(example_path)
    policy_list, event_restriction_fn = get_policy(example_path)

    # make a results directory
    if not osp.isdir(osp.join(config_obj.example_path, 'results')):
        os.mkdir(osp.join(config_obj.example_path, 'results'))

    # Creation of World object
    world_obj = World(config_obj, model, policy_list, event_restriction_fn,
                      agents_filename, interactions_files_list,
                      probabilistic_interactions_files_list,
                      locations_filename, events_files_list,
                      one_time_event_file)

    if vuldetect:
        vd_config_filename = get_config_path(example_path, 'vd_config.txt')
        vd_config_obj = ReadVDConfiguration(vd_config_filename)
        VD_obj = VD(vd_config_obj, world_obj)
        VD_obj.run_vul_detection()

    else:
        world_obj.simulate_worlds()


if __name__ == '__main__':
    main()
