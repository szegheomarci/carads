from abc import ABC


class FileReader:
    _file_reader = None

    def __init__(self, config):
        if config["format"] == "dsv":
            self._file_reader = DSVReader(config["delimiter"])
        elif config["format"] == "json":
            pass
        else:
            print("Unknown format")
            exit(1)

    def read(self, filename) -> dict:
        self._file_reader.readfile(filename)
        return self._file_reader.get_result()


class FileTypeReader(ABC):
    _result = None

    def readfile(self, filename):
        self._result = None

    def get_result(self):
        return self._result


class DSVReader(FileTypeReader):
    delimiter = None
    keys = ["id", "title", "subtitle", "price", "odo", "proddate", "engine", "dealer", "country", "zip", "link"]

    def __init__(self, delimiter):
        self.delimiter = delimiter

    def readfile(self, filename):
        self._result = []
        with open(filename, mode='r', encoding='cp1252') as file:
            # Read lines from the file
            lines = file.readlines()
            # Iterate through each line in the file
            for line in lines:
                # Split the line into values using the custom delimiter
                values = line.strip().split(self.delimiter)
                # Create a dictionary using specified keys and row values
                row_dict = {self.keys[i]: values[i] for i in range(len(self.keys))}
                # Append the dictionary to the list
                self._result.append(row_dict)


class JsonReader(FileTypeReader):
    pass
