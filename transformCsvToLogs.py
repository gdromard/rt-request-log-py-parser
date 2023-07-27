import csv
import os
import re
import collections, functools, operator

from datetime import datetime

##########################
##   Helpers functions  ##
##########################
def apply_regex(input_file, output_file, regex_pattern):
    try:
        # Step 1: Read the content of the input file
        with open(input_file, 'r') as file:
            content = file.read()
        # Step 2: Apply the regex pattern to the content
        result = re.sub(regex_pattern, 'USER_AGENT', content)
        
        # Step 3: Write the resulting content to a new file
        with open(output_file, 'w') as file:
            file.write(result)
        print("Regex applied successfully. Result saved to", output_file)
    except IOError as e:
        print("An error occurred while processing the file:", e)
##########################
##      Main logic      ##
##########################
#df = pd.read_csv("C:/Users/Marek/Downloads/0deg-5ms.csv", skiprows=5,  delimiter=',(?![^\(]*[\)])', engine="python")

csvs_directory = "csv_to_transform"

# process all files in directory
for root,dirs,files in os.walk(csvs_directory):
    for file in files:
       
       if file.endswith(".csv"):
           file_path = os.path.join(csvs_directory, file)
           # Here we repplcae systematically the content between parenthesis as it contains comma very often 
           regex_pattern = r'\(.*?\)'
           print(f"processing {file_path}")
           name_split = os.path.splitext(file_path)
           output_file_name = name_split[0] + '-request.log'
           apply_regex(file_path, output_file_name, regex_pattern)
