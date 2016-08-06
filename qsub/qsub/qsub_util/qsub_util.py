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
import sys


class qsub_util:
    """
    A class to make submitting jobs with qsub easier.
    """
    def __init__(self, command_file, dependency_file, mem_file, wd=None):
        if wd is not None:
            self.wd = wd
        try:
            print("Hi!")
            with open(command_file, 'r') as commandf, open(dependency_file, 'r') as depf, open(mem_file, 'r') as memf:
                print('Reading Inputs...')
                self.com_lines = commandf.read().splitlines()

                try:
                    self.dep_lines = [int(i) if i else None for i in [re.sub('\\s+', '', i) for i in depf.read().splitlines()]]
                except ValueError as e:
                    print("You have passed an invalid line in your dependencies file. \n"+
                          "Is one of your lines not an Integer?")
                    
                    sys.exit(1)
                try:
                    self.mem_lines = [str(i) if i else None for i in [re.sub('\\s+', '', i) for i in memf.read().splitlines()]]
                except ValueError as e:
                    print("You have passed an invalid line in your memory file.")
                    #print ('Operation failed: %s', e.strerror)
                    sys.exit(1)
                if ((len(self.com_lines) == len(self.dep_lines))
                        and (len(self.dep_lines) == len(self.mem_lines))):
                    print('Everything is good!')
                else:
                    ermsg = ('\tlen(command lines) = %d, len(dependency lines) ' +\
                            '= %d, len(memory lines) = %d') % (len(self.com_lines),
                            len(self.dep_lines), len(self.mem_lines))
                    raise ValueError('The dimensions of your input files are not correct. \n' + ermsg)
                self.job_ids = [None] * len(self.com_lines)
            
        except IOError as e:
            print('One of your files is unreadable.')
            print(e)
            sys.exit(1)
        pass

    def submit_execution_chain(self):
        """
        Submits jobs serially using qsub to the cluster.
        """
        # sort by the dependencies, so all deps will have
        # been run by time we get to a new command.
        order = sorted(range(len(self.dep_lines)), key=lambda x:self.dep_lines[x])

        self.dep_lines = sorted(self.dep_lines)

        self.com_lines = [ self.com_lines[i] for i in order] # rearrange
        self.mem_lines = [ self.mem_lines[i] for i in order] # rearrange

        if(len(self.com_lines) < max(self.dep_lines)):
            raise ValueError(('You have a dependency for line %s with ' +
                              'only %s commands.')% 
                              (max(self.dep_lines),
                               len(self.com_lines)))
        for i in range(0, len(self.com_lines)):
            cmd = self.com_lines[i]
            mem = self.mem_lines[i]
            dep = self.dep_lines[i]
            request = "echo -e \'#!/bin/bash\n" + cmd + "\' "
            qsub_cmd = request + " | qsub "
            if (mem is not None): qsub_cmd += (" -l h_vmem=" + mem)
            if (self.wd is not None): qsub_cmd += (" -o " + self.wd + " -e " + self.wd)
            if (dep is not None): qsub_cmd += (" -hold_jid " + self.job_ids[dep])

            print(qsub_cmd)
            (out, err) = execute_cmd(qsub_cmd)
            self.job_ids[i] = re.search('(?<=Your job )(.*?)(?= )', out).group(0)
        pass

def execute_cmd(cmd):
    """
        Executes a command.
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    code = p.returncode
    if code:
        sys.exit("Error " + str(code) + ": " + err)
    return out, err
