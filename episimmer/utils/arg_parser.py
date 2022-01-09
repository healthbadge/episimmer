import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser()

    # input argument options
    arg_parser.add_argument(dest='example_path',
                            type=str,
                            help='Pass the path to the data folder')
    arg_parser.add_argument(
        '-np',
        '--noplot',
        dest='noplot',
        action='store_false',
        default=True,
        help='Restrict plotting the time plot after simulation. Default = False'
    )
    arg_parser.add_argument(
        '-vul',
        '--vuldetect',
        dest='vuldetect',
        action='store_true',
        default=False,
        help=
        'Run Vulnerability Detection on the data folder based on VD_config.txt. Default = False'
    )
    arg_parser.add_argument(
        '-a',
        '--animate',
        dest='animate',
        action='store_true',
        default=False,
        help='Creates a gif animation of the time plot. Default = False')
    arg_parser.add_argument('-s',
                            '--stats',
                            dest='stats',
                            action='store_true',
                            default=False,
                            help='Choose to store statistics. Default = False')
    arg_parser.add_argument(
        '-viz',
        '--vizdyn',
        dest='viz_dyn',
        action='store_true',
        default=False,
        help=
        'Creates a gif of the simulation environment progressing through the days. Default = False'
    )
    args = arg_parser.parse_args()
    return args
