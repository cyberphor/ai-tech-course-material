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
# contain the word "confidential". The list should be printed to the terminal.

# Your task is to write the command so that:
#     - it matches the word "confidential"
#     - the matching is case-insensitive, i.e., not only "confidential" is
#       matched but also variations such, e.g., "Confidential", "CONFIDENTIAL",
#       "CoNfIdEnTiAl", etc.

# You are expected to solve this problem using the `grep` command. However, it
# is ok to use a different tool provided the tool would be available in standard
# debian-based linux distribution.

# Try searching the options of GNU grep from the manual page,
# 1. Display the manual page for "grep": man grep
# 2. Hit "/", type in the keyword and hit "Enter"
# 3. Hit "n" to find the next match and "N" to find the previous match

# Hint: search keyword "case" to find all the options related to "case"

grep -i -r -l "confidential" emails
