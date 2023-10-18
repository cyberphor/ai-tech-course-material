from datetime import datetime
import os
import random

def create_dev_set(full_data_dir, dev_data_dir, ratio=10):
    os.makedirs(dev_data_dir, exist_ok=True)
    for file_name in sorted(os.listdir(full_data_dir)):
        with open(f'{full_data_dir}/{file_name}') as file_full,\
                open(f'{dev_data_dir}/{file_name}', 'w') as file_dev:
            for line in file_full:
                rand_num = random.randint(0, 100)
                if rand_num < ratio:
                    file_dev.write(line)

# TODO 1: Place your code here.
def load_phone_calls_dict(data_dir: str) -> dict:
    # Assign a phone_calls_dict variable with an empty dict.
    phone_calls_dict = dict()
    # Implement a for loop that iterates over the phone_calls_*.txt files.
    # HINT: The os.listdir function may be helpful here.
    for f in os.listdir(data_dir):
        if f.endswith(".txt"):
            # For each file, open it (preferably using the with statement)
            # and read it line by line.
            file_path = data_dir + "/" + f
            with open(file_path, "r") as file_stream:
                for line in file_stream.readlines():
                    # Extract the timestamp and the phone_number from each line
                    # into separate variables. HINT: Use the split method to
                    # separate a line into the two constituents.
                    timestamp, phone_number = line.strip().split(": ")
                    # From the phone_number extract the area_code.
                    # HINT: Use slicing on the str which can be understood as
                    # a list of characters. You want to extract the three digits
                    # enclosed in the parentheses.
                    area_code = phone_number.split("(")[1].split(")")[0]
                    # Cast the timestamp into the datetime object. This will
                    # enable you to easily determine if the call happened after
                    # a certain hour in a day. HINT: You have done this in the
                    # preceding module.
                    date_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    # Check if the phone call happened between midnight
                    # (included) and 6 am (not included).
                    if (date_time.hour >= 0) and (date_time.hour < 6):
                        # Use conditional statements to check if the necessary
                        # keys are already present in the phone_calls_dict. If
                        # the phone call happened between midnight and 6 am
                        # append the timestamp to the appropriate place in the
                        # phone_calls_dict.
                        if area_code in phone_calls_dict.keys():
                            if phone_number in phone_calls_dict[area_code].keys():
                                phone_calls_dict[area_code][phone_number].append(date_time)
                            else:
                                phone_calls_dict[area_code][phone_number] = list()
                                phone_calls_dict[area_code][phone_number].append(date_time)
                        else:
                            phone_calls_dict[area_code] = dict()
                            phone_calls_dict[area_code][phone_number] = list()
                            phone_calls_dict[area_code][phone_number].append(date_time)
    return phone_calls_dict

# TODO 2: Place your code here.
def generate_phone_call_counts(phone_calls_dict: dict) -> dict:
    call_counts = dict()
    for area_code in phone_calls_dict:
        for phone_number in phone_calls_dict[area_code]:
            call_counts[phone_number] = len(phone_calls_dict[area_code][phone_number])
    return call_counts

# TODO 3: Place your code here.
def most_frequently_called(phone_call_counts: dict, top_n: int) -> list:
    phone_calls = list()
    for phone_call, count in phone_call_counts.items():
        phone_calls.append((phone_call, count))
    phone_calls_sorted_by_number = sorted(phone_calls, key = lambda phone_call: phone_call[0])
    phone_calls_sorted = sorted(phone_calls, key = lambda phone_call: (-phone_call[1], phone_call[0]))
    most_called = phone_calls_sorted[0:top_n]
    return most_called

# TODO 4: Place your code here.
def export_phone_call_counts(most_frequent_list: list, out_file_path: str):
    # Open the out_file_path for writing, preferably using the with statement.
    with open(out_file_path, "w") as stream:
        # Iterate over the elements of the most_frequent_list.
        for phone_number in most_frequent_list:
            # In each iteration write the entry into the file (single line)
            # in the specified format.
            stream.write(f"{phone_number[0]}: {phone_number[1]}\n")

# TODO 5: Place your code here.
def export_redials_report(phone_calls_dict: dict, report_dir: str):
    # If report_dir doesn't exist, you need to create the folder and write files
    # within it.
    if not os.path.isdir(report_dir):
        os.makedirs(report_dir)
    # Iterate over the phone_calls_dict where in each iteration you assign the
    # area_code with the key of the dictionary, and ac_data with the
    # corresponding value.
    for area_code in phone_calls_dict:
        # Write the output into the respective <area_code>.txt file. If there is
        # no output, just create an empty <area_code>.txt file.
        file_path = report_dir + '/' + str(area_code) + ".txt"
        with open(file_path, "w") as file_stream:
            # Since ac_data is also a dict, create a nested loop over ac_data.
            # In each iteration a key is assigned to phone_number and a
            # corresponding value to call_data.
            for phone_number in phone_calls_dict[area_code]:
                # Finally, iterate over the call_data (sorted). Note that within
                # each iteration you need to work with two consecutive
                # timestamps. For example, in the first iteration you would like
                # to compare the first timestamp with the second one. In the
                # second iteration you would like to compare the second one to
                # the third. And so on, ... This may be a bit challenging for
                # you to figure out. However, we also believe it would be a
                # worthwhile effort. Hence, we do not provide any further hints
                # on this point.
                call_data = sorted(phone_calls_dict[area_code][phone_number], key = lambda call: str(call).split()[0])
                total_calls = len(call_data)
                for call in call_data:
                    try:
                        next_call = call_data[call_data.index(call) + 1]
                    except IndexError:
                        break
                    # Assuming in each iteration you have the timestamp_1 and
                    # timestamp_2 that are both datetime objects you can
                    # Use the sec_diff, phone_number, timestamp_1, and
                    # timestamp_2 to produce a desired output (i.e., the
                    # instances where a number was redialed in less than 10
                    # minutes)
                    time_between_calls = (next_call - call).total_seconds()
                    if time_between_calls > 0 and time_between_calls < 600:
                        call = str(call)
                        call_day = call.split()[0]
                        call_time = call.split()[1]
                        next_call_time = str(next_call).split()[1]
                        minutes, seconds = divmod(time_between_calls, 60)
                        file_stream.write(f"{phone_number}: {call_day} {call_time} -> {next_call_time} ({int(minutes):0>2}:{int(seconds):0>2})\n")
                        # +1(892)532-9243: 2020-01-01 00:00:09 -> 00:01:20 (01:11)