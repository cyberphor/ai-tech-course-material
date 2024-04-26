"""Module for Task 3"""

import os
import re


def get_unique_email_addresses(
    source_directory: str = "enron_berkeley_subset",
    destination_file: str = "enron_email_list.txt",
):
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    email_addresses = set()
    for file in os.listdir(source_directory):
        with open(f"{source_directory}/{file}", "r", encoding="UTF-8") as email:
            email_addresses.update(
                [match.lower() for match in re.findall(pattern, email.read())]
            )
    with open(destination_file, "w", encoding="UTF-8") as output:
        for email_address in sorted(email_addresses):
            output.write(f"{email_address}\n")


if __name__ == "__main__":
    get_unique_email_addresses()
