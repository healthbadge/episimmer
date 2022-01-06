import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(
        prog='Main.py', usage='%(prog)s example_path [options]')

    # input argument options
    arg_parser.add_argument(dest="example_path", type=str,
                            help="Pass the path to your data folder")
    arg_parser.add_argument("-np", "--noplot", dest="noplot",
                            action="store_false", default=True,
                            help="Doesn't show plot after simulation")
    arg_parser.add_argument(
        "-vul", "--vuldetect", dest="vuldetect", action="store_true",
        default=False,
        help="Run Vulnerability Detection on data folder based on VD_config.txt"
    )
    arg_parser.add_argument("-an", "--animate", dest="animate",
                            action="store_true", default=False,
                            help="Creates gif animation in the example folder")
    arg_parser.add_argument("-s", "--stats", dest="stats", action="store_true",
                            default=False,
                            help="Choose to store statistics. Default = False")
    arg_parser.add_argument(
        "-vd", "--vizdyn", dest="viz_dyn", action="store_true", default=False,
        help="Choose to vizualize simulation dynamically. Default = False")
    args = arg_parser.parse_args()
    return args
