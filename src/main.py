import os
import shutil
import time
import yaml
import build_list
import db_actions
from src.db_updater import DBUpdater
from src.file_reader import FileReader


def read_files() -> None:
    pass


config_file = "config/config.yaml"
try:
    with open(config_file, 'r') as yaml_file:
        # Load the YAML data
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        cfg_source = config["source"]
        cfg_database = config["database"]
#        print(config.get('source').get('delimiter'))
#        print(config['source']['delimiter'])
except FileNotFoundError:
    print(f"File '{config_file}' not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error reading YAML file: {e}")
    exit(1)

db_updater = DBUpdater(cfg_database)

# read the source
if cfg_source["type"] == "file":
    # For file based input, the input folder is read continuously and if there are files, they are read and the
    # content is imported one by one. After a file is processed, it is moved into the processed folder.
    file_reader = FileReader(cfg_source)
    file_path = "input/"
    processed_folder = "processed/"
    # read files from ./input
    while True:
        try:
            # Get a list of files in the directory sorted alphabetically
            files = sorted(os.listdir(file_path))
            # Check if there are files in the directory
            if files:
                for file in files:
                    print(f"processing {file_path}{file}")
                    results = file_reader.read(file_path + file)
                    db_updater.update_db(file.split('.')[0], results)
                    shutil.move(file_path + file, processed_folder)
            else:
                time.sleep(60)  # Wait for a minute before checking again
        except FileNotFoundError:
            print("Directory input not2 found.")
        except PermissionError:
            print("You don't have permission to access ./input.")
        except Exception as e:
            print(f"An error occurred: {e}")
elif cfg_source["type"] == "kafka":
    results = build_list.from_kafka()




# load into database


exit(0)
# Example usage
file_name = 'test/20231021_134742.txt'  # Replace 'example.txt' with your CSV file path
input_name = 'import_20231021_134742'
start_date = '2023-10-21'
custom_delimiter = '####'  # Specify the custom delimiter used in your CSV file
header_keys = ["id", "title", "subtitle", "price", "odo", "proddate", "engine", "dealer", "country", "zip",
               "link"]  # Specify the keys for the dictionaries

# read the file
results = build_list.read_delimited_file(file_name, custom_delimiter, header_keys)

db_loader = db_actions.DatabaseLoader("192.168.0.160", 3306, "chaz3app", "chaz3app", "db")
db_loader.create_import_table(input_name, start_date)
db_loader.insert_list(input_name, results)
