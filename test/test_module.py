import unittest
import sys
import sinon
import os

sys.path += ['../lib']
import kpygpio;

#basic gpio test
class TestBasicGPIO(unittest.TestCase):


    def test_init(self):
        stubfd = os.open('/home/kevin/Documents/workspace/pygpio/test/test_cpu_info.txt', os.O_ASYNC | os.O_RDONLY)
        stub = sinon.stub(os, 'open').returns(stubfd)
        pygpio_test = kpygpio.Kpygpio()
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
