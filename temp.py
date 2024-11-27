def read_input_file(file_path):
        with open(file_path, 'r') as file:
            input_lines = file.readlines()
        return [line.strip() for line in input_lines]

input_file = "input_dimensions/merchant_id.txt"
test_list = read_input_file(input_file)
print(test_list)