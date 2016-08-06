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
from qsub.scripts.qsub_submit import qsub_submit
from qsub.qsub_util import qsub_util as qsu
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
        fcmd = open(cmdfn, 'w')
        fcmd.writelines('%s\n' % cmd for cmd in ['cat ' + test + '.txt >> testo.txt' for test in self.test_files])
        fdep = open(depfn, 'w')
        fdep.writelines('%s\n' % dep for dep in ['4', '', '', '2', '', ''])

        fmem = open(memfn, 'w')
        fmem.writelines('%s\n' % mem for mem in ['', '', '', '1MB', '', ''])

        wd, err = execute_cmd('pwd')
        wd = wd.rstrip()

        print(open(cmdfn, 'r').readlines())

        sub = qsu(wd + "/" + cmdfn, wd + "/" + depfn, wd + "/" + memfn, wd=wd)
        sub.submit_execution_chain()
        pass


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0], '-v'])
