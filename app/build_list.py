def read_delimited_file(file_path, delimiter, keys):
    data = []
    with open(file_path, mode='r') as file:
        # Read lines from the file
        lines = file.readlines()
        # Iterate through each line in the file
        for line in lines:
            # Split the line into values using the custom delimiter
            values = line.strip().split(delimiter)
            # Create a dictionary using specified keys and row values
            row_dict = {keys[i]: values[i] for i in range(len(keys))}
            # Append the dictionary to the list
            data.append(row_dict)
    return data


def from_file():
    pass


def from_kafka():
    pass
