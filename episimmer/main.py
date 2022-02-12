import os
import os.path as osp

from episimmer.read_file import ReadConfiguration, ReadVDConfiguration
from episimmer.utils.arg_parser import parse_args
from episimmer.utils.module_handling import get_model, get_policy
from episimmer.utils.statistics import write_stats
from episimmer.vulnerability_detection.vd import VD
from episimmer.world import World


def get_world_obj(config_obj, example_path):
    """
    Returns the world object for the simulation

    Args:
        config_obj: Config object populated with configuration from the config.txt file
        example_path: Path to directory with simulation files

    Returns:
        World object
    """
    agents_filename, interactions_files_list_filename, \
        events_files_list_filename, locations_filename, \
        one_time_event_file, probabilistic_interactions_files_list_filename = config_obj.get_file_paths(example_path)
    interactions_files_list, events_files_list, \
        probabilistic_interactions_files_list = config_obj.get_file_names_list(
                                                        example_path, interactions_files_list_filename,
                                                        events_files_list_filename,
                                                        probabilistic_interactions_files_list_filename)

    # User Model and Policy
    model = get_model(example_path)
    policy_list = get_policy(example_path)

    # make a results directory
    if not osp.isdir(osp.join(config_obj.example_path, 'results')):
        os.mkdir(osp.join(config_obj.example_path, 'results'))

    # Creation of World object
    world_obj = World(config_obj, model, policy_list, agents_filename,
                      interactions_files_list,
                      probabilistic_interactions_files_list,
                      locations_filename, events_files_list,
                      one_time_event_file)

    return world_obj


@write_stats('stats.pickle', 'stats.txt')
def main():
    """
    Episimmer run begins here.
    """
    args = parse_args()

    example_path = args.example_path
    vul_detect = args.vuldetect
    config_obj = ReadConfiguration(osp.join(example_path, 'config.txt'))
    world_obj = get_world_obj(config_obj, example_path)

    if vul_detect:
        vd_config_filename = osp.join(example_path, 'vd_config.txt')
        vd_config_obj = ReadVDConfiguration(vd_config_filename)
        vd_obj = VD(vd_config_obj, world_obj)
        vd_obj.run_vul_detection()

    else:
        world_obj.simulate_worlds()


if __name__ == '__main__':
    main()
