import unittest
import subprocess
import os
import os.path as osp


class TestExamples(unittest.TestCase):

    # Classic Testing
    def test_examples(self):
        print()
        sub_examples_list = [
            s for s in os.listdir('examples')
            if osp.isdir(osp.join('examples', s))
        ]
        for j in sub_examples_list:
            examples_list = [
                p for p in os.listdir(osp.join('examples', str(j)))
                if osp.isdir(osp.join('examples', str(j), p))
                and osp.isfile(osp.join('examples', str(j), p, 'config.txt'))
            ]
            for i, example in enumerate(examples_list):
                main_path = osp.join('src', 'Main.py')
                example_path = osp.join('examples', j, example)
                process = subprocess.run(
                    'python3 {0} {1} -np'.format(main_path, example_path),
                    shell=True, stdout=subprocess.DEVNULL)
                if (process.returncode):
                    raise Exception(
                        'Example {0} could not be run!'.format(example))
                print(
                    'Classic Testing : {1}/{2} - {0} - {3} - complete'.format(
                        j, i + 1, len(examples_list), example))

    # Vulnerability Detection Testing
    def test_vd_examples(self):
        print()
        examples_list = [
            p for p in os.listdir(
                osp.join('examples', 'Vulnerability_Detection')) if osp.isfile(
                    osp.join('examples', 'Vulnerability_Detection', p,
                             'vd_config.txt'))
        ]
        for i, example in enumerate(examples_list):
            main_path = osp.join('src', 'Main.py')
            example_path = osp.join('examples', 'Vulnerability_Detection',
                                    example)
            process = subprocess.run(
                'python3 {0} {1} -vul'.format(main_path, example_path),
                shell=True, stdout=subprocess.DEVNULL)
            if (process.returncode):
                raise Exception(
                    'Example {0} could not be run!'.format(example))
            print('Vulnerability Detection Testing : {0}/{1} - {2} - complete'.
                  format(i + 1, len(examples_list), example))


if __name__ == '__main__':
    unittest.main()
