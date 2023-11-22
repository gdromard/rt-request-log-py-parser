import csv
import os
import collections, functools, operator
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

def process_current_file(file, inbound_dict_list, outbound_dict_list, dialect='piper'):
    with open(file, "r") as csvfile:
        for row in csv.DictReader(csvfile, dialect=dialect, fieldnames=fieldnames):
            log_timestamp = row['timestamp']
            http_method = row['request_method']
            
            # in bytes, can be either inbound or outbound in these logs format version
            current_length = int(row['content_length'])
            dt = datetime.strptime(log_timestamp, "%Y%m%d%H%M%S")
            aggregated_log_key = str(dt.month) + "-" + str(dt.year)
            # now we add the current metric if relevant to the appropriate dict list,
            # and we ignore HEAD requests as we don't charge our customers for them
            if ((http_method == "GET") and (current_length > 0)):
                outbound_dict_list.append({aggregated_log_key : current_length})
            elif (http_method != "HEAD" and (current_length > 0)):
                inbound_dict_list.append({aggregated_log_key : current_length})
    return
##########################
##      Main logic      ##
##########################

logs_directory = "logs_to_process"
csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
csv.register_dialect('comma', delimiter=',', quoting=csv.QUOTE_NONE)

fieldnames = ['timestamp' ,'request_time','log_type','remote_address','username ','request_method','request_url','http_version','return_status','content_length']

inbound_dict_list = []
outbound_dict_list = []

# process all files in directory
for root,dirs,files in os.walk(logs_directory):
    for file in files:
       
       if file.endswith(".log"):
           file_path = os.path.join(logs_directory, file)
           print(f"processing {file_path}")
           # change separator if needed
           process_current_file(file_path, inbound_dict_list, outbound_dict_list, 'piper')

    inbound_aggregation = dict(functools.reduce(operator.add,
            map(collections.Counter, inbound_dict_list)))
    outbound_aggregation = dict(functools.reduce(operator.add,
            map(collections.Counter, outbound_dict_list)))
    
    print(Fore.GREEN + "Total Inboud results per month")
    display_results(inbound_aggregation)
    print(Fore.GREEN + "Total Outboud results per month")
    display_results(outbound_aggregation)    
    