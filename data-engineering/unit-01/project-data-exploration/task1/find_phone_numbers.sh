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

# Your task is to list the names of files in the ./emails/ directory that
# contain phone numbers. The list should be printed to the terminal.

# You are expected to solve this problem using the `grep` command. However, it
# is ok to use a different tool provided the tool would be available in standard
# debian-based linux distribution.

# Your task is to write the command so that:
#     - it goes over all the files in the `emails` directory
#     - the outputs are just names of the files with matches (not the matched
#       lines themselves).

# Use `man grep` to access `grep` manual.

# Hint1: You need a write a regex to match phone numbers.
#        You can use the following regex '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b'
#        to implement this search.

# Hint2: Use '-P' flag for signifying regex pattern

grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails