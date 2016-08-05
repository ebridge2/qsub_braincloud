#!/usr/local/bin/python

# a utility to submit a series of expressions to the
# cluster through qsub.
#
# Inputs:
#   $1: text file: Each file represents the 
#   $2: text file: Each file represents the line
#           number of its dependency. For example, if
#           line 1 is a preprocessing script on raw data and line 6
#           is a registration script that depends on the output of
#           line 1, you would write: "" on line 1, and "0" on line
#           6. Note that we ZERO INDEX the dependencies (ie,
#           line 1 would have a value of 0, not 1).
#       
#   $3: text file: each line is the memory requirements
#           for the specific job to conduct. If no
#           entry is present, runs without memory allocation.
#
# Note: Only spent a little bit of time on this, so if you make
#   improvements, please PR!
#

from argparse import ArgumentParser
from subprocess import Popen, PIPE
import numpy as np
import re


class qsub_util:
    """
    A class to make submitting jobs with qsub easier.
    """
    def __init__(self, command_file, dependency_file, memory_file, wd=None):
        try:
            with open(command_file) as commandf, open(dependency_file) as depf, open(mem_file) as memf:
                print('Reading Inputs...')
                self.com_lines = commandf.readlines()
                try:
                    self.dep_lines = [int(i) if not i else None for i in [re.sub('\\s+', None, i) for i in depf.readlines()]]
                except ValueError as e:
                    print("You have passed an invalid line in your dependencies file. \n"+
                          "Is one of your lines not an Integer?")
                    print('Operation failed: %s', e.strerror)
                    sys.exit(1)
                try:
                    self.mem_lines =  [str(i) if not i else None for i in [re.sub('\\s+', '', i) for i in memf.readlines()]]
                except ValueError as e:
                    print("You have passed an invalid line in your memory file.")
                    print ('Operation failed: %s', e.strerror)
                    sys.exit(1)
                if ((length(com_lines) == length(dep_lines))
                        and(length(dep_lines) == length(mem_lines))):
                    print('Everything is good!')
                else:
                    raise ValueError('The dimensions of your input files are not correct.')
                self.job_ids = [None] * length(self.com_lines)
        except IOError as e:
            print('Operation failed: %s', e.strerror)

    def submit_execution_chain(self):
        """
        Submits jobs serially using qsub to the cluster.
        """
        order = sorted(self.dep_lines) # sort by the dependencies, so all deps will have
                                       # been run by time we get to a new command.
        self.com_lines = self.com_lines[order] # rearrange
        self.mem_lines = self.mem_lines[order] # rearrange

        if(length(self.com_lines) < max(self.dep_lines)):
            raise ValueError(('You have a dependency for line %s with ' +
                              'only %s commands.')% 
                              (max(self.dep_lines),
                               length(self.com_lines)))
        for i in range(0, length(self.com_lines)):
            cmd = self.com_lines[i]
            mem = self.mem_lines[i]
            dep = self.dep_lines[i]
            qsub_cmd = "echo " + cmd + " | "
            if (mem is not None): qsub_cmd += (" -l h_vmem=" + mem)
            if (dep is not None): qsub_cmd += (" -W depend=afterok:" + self.job_ids[dep])
            if (self.wd is not None): qsub_cmd += (" -o " + self.wd + " -e " + self.wd)
            self.job_ids[i] = self.execute_cmd(qsub_cmd)
        pass

    def execute_cmd(self, cmd):
        """
            Executes a command.
        """
        p = Popen(cmd, stdout=PIPE, shell=True)
        out, err = p.communicate()
        code = p.returncode
        if code:
            sys.exit("Error " + str(code) + ": " + err)
        return out, err
