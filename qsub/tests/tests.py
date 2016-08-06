#!/usr/bin/env python

#
# A basic set of tests to verify that
# the qsub utility is working properly.
# submits some simple jobs to the job
# execution service and makes sure they work.
#
# written by Eric Bridgeford

import unittest
import sys
sys.path.insert(0, '../')
from subprocess import Popen, PIPE
import qsub
from qsub import qsub_submit as qsu
from qsub import execute_cmd


class TestQsubUtility(unittest.TestCase):
    def setUp(self):
        self.test_files = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6']
        cmd = 'rm -f *.txt'
        execute_cmd(cmd)
        for tf in self.test_files:
            cmd = 'echo ' + '\"' + tf + '\" > ' + tf + '.txt'
            execute_cmd(cmd)
        pass

    def tearDown(self):
        cmd = 'rm -f *.txt'
        # execute_cmd(cmd)
        pass

    def test_all(self):
        cmdfn = 'cmd.txt'
        depfn = 'dep.txt'
        memfn = 'mem.txt'

        wd, err = execute_cmd('pwd')
        wd = wd.rstrip()

        fcmd = open(cmdfn, 'w')
        fcmd.writelines('%s\n' % cmd for cmd in ['echo \"$(cat ' + wd + "/" + test + '.txt)\" >> ' + wd + '/testo.txt' for test in self.test_files])
        fdep = open(depfn, 'w')
        fdep.writelines('%s\n' % dep for dep in ['4', '', '', '2', '', ''])

        fmem = open(memfn, 'w')
        fmem.writelines('%s\n' % mem for mem in ['', '', '', '', '', ''])

        fcmd.close()
        fdep.close()
        fmem.close()

        qsu(wd + "/" + cmdfn, wd + "/" + depfn, wd + "/" + memfn, wd=wd)
        while(execute_cmd('qstat')[0] != ''):
            execute_cmd("sleep 10") # check again in 10 seconds
        execute_cmd("sleep 10") # sometimes opening this file too soon is bad :(
        with open('testo.txt', 'r') as fout:
            prod = fout.read().splitlines()

            self.assertEqual(prod[4], 'test4')
            self.assertEqual(prod[5], 'test1')
        pass


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0], '-v'])
