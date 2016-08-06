#!/usr/bin/env python
#
# A script to submit a series of jobs to qsub
# using the qsub_util class.
#
# written by Eric Bridgeford on 08/05/16

from argparse import ArgumentParser
from qsub.qsub_util import qsub_util


def qsub_submit(command_file, dep_file, mem_file, wd=None):
    job_submit = qsub_util(command_file, dep_file, mem_file, wd)
    job_submit.submit_execution_chain()

def main():

    parser = ArgumentParser()
    parser.add_argument("command_file", help="File where each line is a " +
                        "command to run.")
    parser.add_argument("dep_file", help="File where each line is None or the " +
                        "line of a dependency.")
    parser.add_argument("mem_file", help ="File where each line "+
                        "corresponds to the memory requirement for a command")
    parser.add_argument("-w", "--working_dir", help="The working directory "+
                        " in which to execute commands.")
    parser.parse_args()

    self.qsub_submit(parser.command_file, parser.dep_file, parser.mem_file,
                wd=parser.working_dir) 

if __name__ == "__main__":
    main()
