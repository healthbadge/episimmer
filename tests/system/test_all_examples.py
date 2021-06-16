import unittest
import subprocess
import os

class TestExamples(unittest.TestCase):
    def test_examples(self):
        examples_list = [p for p in os.listdir("examples") if os.path.isdir(os.path.join("examples",p))]

        for example in examples_list:
            main_path = os.path.join("src","Main.py")
            example_path = os.path.join("examples",example)
            # error = os.system("python3 {0} {1} -noplot".format(main_path,example_path))
            process = subprocess.run("python3 {0} {1} -noplot".format(main_path,example_path),shell=True)
            if(process.returncode):
                raise Exception('Example {0} could not be run!'.format(example))



if __name__ == '__main__':
    unittest.main()
