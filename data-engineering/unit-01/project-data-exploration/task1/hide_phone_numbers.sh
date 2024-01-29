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

# Your task is to transform the data set so that it can be released to the
# public. This practically means that you would like to replace all the emails
# with <EMAIL_REMOVED> token and all the phone numbers with <PHONE_REMOVED>
# token.

# Your task is to finish the code so that:
#     - it replaces email addresses with the <EMAIL_REMOVED> token (already
#       done)
#     - it replaces phone numbers with the <PHONE_REMOVED> token (your task)
#     - the newly created files have the same names as the original ones and
#       they are stored in the `anon_emails` directory.

# You are expected to solve this problem using the `sed` command. However, it
# is ok to use a different tool provided the tool would be available in standard
# debian-based linux distribution.

# You are provided with the boilerplate code below. Your task is to replace the
# YOUR_SOLUTION_HERE token. It should not be necessary to do any other changes
# to the code. However, you can do whatever changes you deem fit as long as you
# end up with an equivalent solution.

# Hint: To match phone numbers, use the regular expression that was used in the
# previous exercises. However, note that `sed` does not interpret the \d as we would need it to.
# Hence, you need to replace the \d parts of the regular expression with an
# equivalent (think character classes).

mkdir -p anon_emails
for file_name in emails/*; do
    sed -r 's/[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+/<EMAIL_REMOVED>/gI' "$file_name" > anon_"$file_name"
    cp anon_"$file_name" anon_"$file_name"_
    sed -r 's/\b[0-9]{3}\W*[0-9]{3}\W*[0-9]{4}\b/<PHONE_REMOVED>/gI' anon_"$file_name"_ > anon_"$file_name"
    rm anon_"$file_name"_
done