import os
import os.path as osp
import subprocess
import unittest


class TestExamples(unittest.TestCase):

    # Classic Testing
    # def test_examples(self):
    #     """
    #     Running classic simulation
    #     """
    #     print()
    #     sub_examples_list = [
    #         s for s in os.listdir('examples')
    #         if osp.isdir(osp.join('examples', s))
    #     ]
    #     for j in sub_examples_list:
    #         examples_list = [
    #             p for p in os.listdir(osp.join('examples', j))
    #             if osp.isdir(osp.join('examples', j, p))
    #             and osp.isfile(osp.join('examples', j, p, 'config.txt'))
    #         ]
    #         for i, example in enumerate(examples_list):
    #             main_path = osp.join('episimmer', 'main.py')
    #             example_path = osp.join('examples', j, example)
    #             process = subprocess.run('python3 {0} {1} -np'.format(
    #                 main_path, example_path),
    #                                      shell=True,
    #                                      stdout=subprocess.DEVNULL)
    #             if (process.returncode):
    #                 raise Exception(
    #                     'Example {0} could not be run!'.format(example))
    #             print(
    #                 'Classic Testing : {1}/{2} - {0} - {3} - complete'.format(
    #                     j, i + 1, len(examples_list), example))
    #     print('Classic Testing complete!')

    # Vulnerability Detection Testing
    def test_vd_examples(self):
        """
        Running vulnerability detection
        """
        print()
        examples_list = [
            p for p in os.listdir(
                osp.join('examples', 'Vulnerability_Detection')) if osp.isfile(
                    osp.join('examples', 'Vulnerability_Detection', p,
                             'vd_config.txt'))
        ]
        for i, example in enumerate(examples_list):
            main_path = osp.join('episimmer', 'main.py')
            example_path = osp.join('examples', 'Vulnerability_Detection',
                                    example)
            process = subprocess.run('python3 {0} {1} -vul'.format(
                main_path, example_path),
                                     shell=True,
                                     stdout=subprocess.DEVNULL)
            if (process.returncode):
                raise Exception(
                    'Example {0} could not be run!'.format(example))
            print('Vulnerability Detection Testing : {0}/{1} - {2} - complete'.
                  format(i + 1, len(examples_list), example))
        print('Vulnerability Detection Testing complete!')

    # # Visualization and Animation
    # def test_viz_examples(self):
    #     """
    #     Running visualization test
    #     """
    #     print()
    #     sub_examples_list = [
    #         s for s in os.listdir('examples')
    #         if osp.isdir(osp.join('examples', s))
    #     ]
    #     j = sub_examples_list[0]
    #
    #     examples_list = [
    #         p for p in os.listdir(osp.join('examples', j))
    #         if osp.isdir(osp.join('examples', j, p))
    #         and osp.isfile(osp.join('examples', j, p, 'config.txt'))
    #     ]
    #     example = examples_list[0]
    #     i = 0
    #     main_path = osp.join('episimmer', 'main.py')
    #     example_path = osp.join('examples', j, example)
    #     process = subprocess.run('python3 {0} {1} -viz -np -a'.format(
    #         main_path, example_path),
    #                              shell=True,
    #                              stdout=subprocess.DEVNULL)
    #     if (process.returncode):
    #         raise Exception('Example {0} could not be run!'.format(example))
    #     print('Dynamic Viz Testing : {0} - complete'.format(example))
    #
    # # Statistics module
    # def test_statistics(self):
    #     """
    #     Running statistics module
    #     """
    #     print()
    #     sub_examples_list = [
    #         s for s in os.listdir('examples')
    #         if osp.isdir(osp.join('examples', s))
    #     ]
    #     j = sub_examples_list[0]
    #
    #     examples_list = [
    #         p for p in os.listdir(osp.join('examples', j))
    #         if osp.isdir(osp.join('examples', j, p))
    #         and osp.isfile(osp.join('examples', j, p, 'config.txt'))
    #     ]
    #     example = examples_list[0]
    #     i = 0
    #     main_path = osp.join('episimmer', 'main.py')
    #     example_path = osp.join('examples', j, example)
    #     process = subprocess.run('python3 {0} {1} -s -np'.format(
    #         main_path, example_path),
    #                              shell=True,
    #                              stdout=subprocess.DEVNULL)
    #     if (process.returncode):
    #         raise Exception('Example {0} could not be run!'.format(example))
    #     print('Statistics Testing : {0} - complete'.format(example))


if __name__ == '__main__':
    unittest.main()
