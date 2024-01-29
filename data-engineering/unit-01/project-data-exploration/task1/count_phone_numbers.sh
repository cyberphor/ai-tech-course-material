#!/bin/bash

################################################################################
##                      Data Engineering Course                               ##
##                                                                            ##
##            Copyright 2022-2023: Data Engineering Course                    ##
##                     Carnegie Mellon University                             ##
##   Unauthorized distribution of copyrighted material, including             ##
##  unauthorized peer-to-peer file sharing, may subject the students          ##
##  to the fullest extent of Carnegie Mellon University copyright policies.   ##
################################################################################

# Your task is to count the files in the ./emails/ directory that
# contain phone numbers. The list should be printed to the terminal.

# Your task is to write the command so that:
#     - it goes over all the files in the `emails` directory
#     - the outputs of the `grep` command are just names of the files with
#       matches (not the matched lines themselves).
#     - the final output is just a single number informing about the number of
#       files with matches (i.e., the number of lines output by the `grep`
#       command)

# You are expected to solve this problem using the `grep` command. However, it
# is ok to use a different tool provided the tool would be available in standard
# debian-based linux distribution.

# Use `man grep` to access `grep` manual.

# Hint1: You have already done this in a question before!

grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails | wc -l