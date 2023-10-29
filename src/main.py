# pip install pymysql
# pip install pyyaml

import yaml
import build_list
import db_actions


config_file = "config/config.yaml"
try:
    with open(config_file, 'r') as yaml_file:
        # Load the YAML data
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        print("YAML data:")
        print(config)
        print(config.get('source').get('delimiter'))
except FileNotFoundError:
    print(f"File '{config_file}' not found.")
except yaml.YAMLError as e:
    print(f"Error reading YAML file: {e}")

exit
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


