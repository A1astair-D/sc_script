import json
from collections import Counter

# Function to count occurrences of each subSystem value
def count_subsystem_occurrences(input_file, output_file):
    try:
        # Read the JSON file
        with open(input_file, 'r') as file:
            data = json.load(file)

        # Filter out objects with scope 'juspay' or 'all'
        # data = [item for item in data if item.get('scope') not in ['juspay']]
        
        # Extract subSystem values
        sub_systems = [item.get('subSystem') for item in data if item.get('subSystem')]
        
        # Count occurrences using Counter
        sub_system_counts = Counter(sub_systems)
        # with open(output_file, 'w') as file:
        #     json.dump(data, file, indent=4)
        print('subSystem occurrences count:')
        for sub_system, count in sub_system_counts.items():
            print(f'{sub_system}: {count}')
    
    except FileNotFoundError:
        print(f'Error: The file {input_file} was not found.')
    except json.JSONDecodeError:
        print('Error: Failed to decode JSON. Ensure the file contains valid JSON.')

# Main execution
if __name__ == '__main__':
    input_file = 'data2.json'
    output_file = "output2.json"
    count_subsystem_occurrences(input_file, output_file)
