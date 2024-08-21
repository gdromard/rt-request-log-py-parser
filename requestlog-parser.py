import csv
import os
import collections
from colorama import Fore
from datetime import datetime

##########################
##   Helpers functions  ##
##########################
def convert_bytes_to_gb(size_in_bytes):
    gb = size_in_bytes / (1024 ** 3)
    return gb

def display_results(transfert_dict):
    for key, value in transfert_dict.items():
        print(Fore.WHITE + "[" + key + "]", convert_bytes_to_gb(value))

def process_current_file(file, inbound_aggregation, outbound_aggregation, dialect='piper'):
    with open(file, "r") as csvfile:
        for row in csv.DictReader(csvfile, dialect=dialect, fieldnames=fieldnames):
            try:
                log_timestamp = row['timestamp']
                http_method = row['request_method']

                # Replace '-' with '0' and convert to integer
                current_inbound_length = int(row['request_content_length']) if row['request_content_length'] != '-' else 0
                current_outbound_length = int(row['response_content_length']) if row['response_content_length'] != '-' else 0

                dt = datetime.strptime(log_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                aggregated_log_key = f"{dt.month}-{dt.year}"

                if http_method != 'HEAD':
                    if current_inbound_length > 0: inbound_aggregation[aggregated_log_key] += current_inbound_length
                    if current_outbound_length > 0: outbound_aggregation[aggregated_log_key] += current_outbound_length
            except ValueError:
                print(Fore.RED + f"Invalid data format in file {file}")
                continue
    return

##########################
##      Main logic      ##
##########################

logs_directory = "logs_to_process"
csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
csv.register_dialect('comma', delimiter=',', quoting=csv.QUOTE_NONE)

fieldnames = ['timestamp', 'trace_id', 'remote_address', 'username ', 'request_method', 'request_url', 'return_status', 'request_content_length', 'response_content_length', 'request_duration', 'request_user_agent']

inbound_aggregation = collections.defaultdict(int)
outbound_aggregation = collections.defaultdict(int)

# process all files in directory
for root, dirs, files in os.walk(logs_directory):
    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(logs_directory, file)
            print(Fore.YELLOW + f"Processing {file_path}...")
            process_current_file(file_path, inbound_aggregation, outbound_aggregation, 'piper')

print(Fore.GREEN + "Total Inbound results per month")
display_results(inbound_aggregation)
print(Fore.GREEN + "Total Outbound results per month")
display_results(outbound_aggregation)
