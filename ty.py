import os
import json
import re

def file_input_to_list_of_lists(input_filename, output_filename, result_list):
    with open(input_filename, 'r') as file:
        funcs = json.load(file)
        for key, val in funcs.items():
            x = re.search("..*AccountDetails$", key)
            y = re.search("..*AccountDetail$", key)
            if x or y:
                result_list.append((key,val))

    # Write the output to the specified file
    # with open(output_filename, 'w') as outfile:
    #     json.dump(result_list, outfile, indent=4)

    # return result_list

input_dir = '/Users/alastair.dsouza/Documents/euler3/euler-api-gateway/tmp/fieldInspector2'
output_dir = 'output_account_details.json'
# file_input_to_list_of_lists(input_dir, output_dir)
result_list = []
output_dir = 'output_account_details.json'

for subdir, _, files in os.walk(input_dir): 
    for file in files:
        if file.endswith(".types.parser.json"):
            input_file_path = os.path.join(subdir, file)
            output_file_path = os.path.join(output_dir, file)
            file_input_to_list_of_lists(input_file_path, output_file_path, result_list)
    with open(output_dir, 'w') as outfile:
        json.dump(result_list, outfile, indent=4)

    for type_name, acc_details in result_list:
        query_object = {
            type_name : acc_details
        }
        query = "Write Json rules for the below object : \n```\n" + json.dumps(query_object, indent=4) + "\n```"
        print(query)