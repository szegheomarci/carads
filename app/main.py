import os
import shutil
import time
import yaml
import build_list
import db_actions
from db_updater import DBUpdater
from file_reader import FileReader


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
            print("files in input:")
            print('\n'.join(os.listdir("input/")))
            print("files in processed:")
            print('\n'.join(os.listdir("processed/")))
            # Get a list of files in the directory sorted alphabetically
            files = sorted(os.listdir(file_path))
            # Check if there are files in the directory
            if files:
                finish = False
                for file in files:
                    print(f"processing {file_path}{file}")
                    if file == "exit":
                        shutil.move(file_path + file, processed_folder)
                        finish = True
                        break
                    results = file_reader.read(file_path + file)
                    db_updater.update_db(file.split('.')[0], results)
                    shutil.move(file_path + file, processed_folder)
                if finish:
                    break
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
