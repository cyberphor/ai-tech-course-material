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

# Your task is to list the names of the courses from the `udemy_courses_v2.csv`
# file that contain the word `Python` and are free (i.e., not paid).

# Your task is to change the command so that:
#     - it matches the courses that contain "Python" in their titles and are
#       offered for free (not paid)
#     - output only the titles of such courses

# You are expected to solve this problem using the `awk` command. However, it is
# ok to use a different tool provided the tool would be available in a standard
# debian-based linux distribution.

# Use `man awk` to access `awk` manual.
# If you find the manual too dense this might be a good resource to go over:
# https://www.tutorialspoint.com/awk/index.htm

awk -F '\t' '$2 ~ /Python/ && $4 == "False" {print $2}' udemy_courses_v2.csv 