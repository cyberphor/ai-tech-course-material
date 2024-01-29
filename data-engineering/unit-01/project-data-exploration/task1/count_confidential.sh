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

# Your task is to count the files in the ./emails/ directory that contain the
# word "confidential". The count (single number) should be printed on the
# terminal.

# Your task is to write the command so that:
#     - it matches the word "confidential"
#     - the matching is case-insensitive, i.e., not only "confidential" is
#       matched but also variations such, e.g., "Confidential", "CONFIDENTIAL",
#       "CoNfIdEnTiAl", etc.
#     - the outputs of the `grep` command are just names of the files with
#       matches (not the matched lines themselves).
#     - the final output is just a single number informing about the number of
#       files with matches (i.e., the number of lines output by the `grep`
#       command)

# You are expected to solve this problem using the `grep` command, the linux
# pipe functionality, and the `wc` command. However, it is ok to use a different
# tool provided the tool would be available in standard debian-based linux
# distribution.

# Use `man grep` to access `grep` manual.
# Use `man wc` to access `wc` manual.

# Hint1: Search how to display count using wc

grep -i -r -l "confidential" emails | wc -l
