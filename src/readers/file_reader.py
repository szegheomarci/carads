import os
import time

from src.readers.AbstractReaderPublisher import ReaderPublisher


class FileReader(ReaderPublisher):

    def __init__(self, config):
        super().__init__(config)
        if config["format"] == "dsv":
            pass
        elif config["format"] == "json":
            pass
        else:
            print("Unknown format")
            exit(1)

    def read_dsv(self):
        delimiter = self._config["delimiter"]
        while True:
            try:
                # Get a list of files in the directory sorted alphabetically
                files = sorted(os.listdir("./import"))

                # Check if there are files in the directory
                if files:
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
                    for file in files:
                        file_name, file_extension = os.path.splitext(file)
                        if file_extension:  # Skip files without extensions
                            print(file_name)
                else:
                    time.sleep(60)  # Wait for a minute before checking again

            except FileNotFoundError:
                print(f"Directory '{directory_path}' not found.")
            except PermissionError:
                print(f"You don't have permission to access '{directory_path}'.")
            except Exception as e:
                print(f"An error occurred: {e}")


