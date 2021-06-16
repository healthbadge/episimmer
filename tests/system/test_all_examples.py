import unittest
import subprocess
import os
import os.path as osp

class TestExamples(unittest.TestCase):
    def test_examples(self):
        examples_list = [p for p in os.listdir("examples") if osp.isdir(osp.join("examples",p))]

        for example in examples_list:
            main_path = osp.join("src","Main.py")
            example_path = osp.join("examples",example)
            process = subprocess.run("python3 {0} {1} -noplot".format(main_path,example_path),shell=True,stdout=subprocess.DEVNULL)
            if(process.returncode):
                raise Exception('Example {0} could not be run!'.format(example))



if __name__ == '__main__':
    unittest.main()