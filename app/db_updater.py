import re

import pymysql

from app.readers.AbstractReaderObserver import ReaderObserver
from app.readers.AbstractReaderPublisher import ReaderPublisher


def format_date(prod_date):
    pattern = re.compile(r'(\d\d)/(\d\d\d\d)')
    date_form = pattern.sub(r'\2-\1-15', prod_date)
    return date_form


def extract_color(link, the_id):
    color = link.replace(the_id, '').split('-')[-2]
    if color == "gasoline":
        return "unknown"
    else:
        return color


def unit_to_int(unit_value):
    # Remove currency symbol, commas, and non-digit characters using regular expression
    cleaned_value = re.sub(r'[^\d]', '', unit_value)
    # Convert the cleaned string to an integer
    try:
        int_value = int(cleaned_value)
        return int_value
    except ValueError:
        # Handle the case where the input is not a valid number
        print("Invalid united value")
        return None


class DBUpdater(ReaderObserver):
    __data_set: dict
    __data_name: str
    __data_date: str

    def __init__(self, config):
        self.connection = pymysql.connect(
            host=config["host"],
            user=config["user"],
            port=config["port"],
            password=config["password"],
            db=config["database"],
            cursorclass=pymysql.cursors.DictCursor
        )

    def __create_import_table(self):
        cursor = self.connection.cursor()
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.__data_name} (
        `asID` varchar(255),
        `Title` varchar(255),
        `Subtitle` varchar(255),
        `Price` varchar(255),
        `Mileage` varchar(255),
        `ManufDate` DATE,
        `Engine` varchar(255),
        `Seller` varchar(255),
        `Country` varchar(255),
        `Address` varchar(255),
        `Link` varchar(255),
        `Color` varchar(255),
        `PriceEuro` INT,
        `MileageKm` INT,
        `Start_Date` DATE DEFAULT '{self.__data_date}'
        )
        '''

        try:
            cursor.execute(create_table_query)
        except Exception as e:
            print(create_table_query)
            print(f"Error: {e}")

        self.connection.commit()
        self.connection.close()

    def __insert_list(self):
        self.connection.ping()
        try:
            with self.connection.cursor() as cursor:
                # Build the SQL query with placeholders for values
                query = (f"INSERT INTO {self.__data_name} (`asID`, `Title`, `Subtitle`, `Price`, `Mileage`, "
                         f"`ManufDate`, `Engine`, `Seller`, `Country`, `Address`, `Link`, `Color`, `PriceEuro`, "
                         f"`MileageKm`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                val = []
                # Iterate through the list of records and execute the query for each record
                for record in self.__data_set:
                    val.append((record.get('id'), record.get('title'), record.get('subtitle'), record.get('price'),
                                record.get('odo'), format_date(record.get('proddate')), record.get('engine'),
                                record.get('dealer'), record.get('country'), record.get('zip'), record.get('link'),
                                extract_color(record.get('link'), record.get('id')), unit_to_int(record.get('price')),
                                unit_to_int(record.get('odo'))))
                cursor.executemany(query, val)
                self.connection.commit()

        except Exception as e:
            print(query)
            print(val)
            print(f"Error: {e}")

    def __do_update(self):
        self.__create_import_table()
        self.__insert_list()
        self.connection.ping()
        try:
            with self.connection.cursor() as cursor:
                # remove duplicates
                query = (f"DELETE t1 FROM {self.__data_name} t1 INNER JOIN {self.__data_name} t2 WHERE t1.id < t2.id "
                         f"AND t1.asID = t2.asID")
                cursor.execute(query)
                self.connection.commit()
                # all ads present in the input table must have NULL End_Date in the ads table
                query = ("UPDATE `ads` SET `End_Date`=NULL WHERE `End_Date` IS NOT NULL AND `asID` IN (SELECT `asID` "
                         "FROM `{self.__data_name}`")
                cursor.execute(query)
                self.connection.commit()
                # active ads in the ads table not present in the input table must be updated with End_Date
                query = (f"UPDATE `ads` SET `End_Date`='{self.__data_date}' WHERE `End_Date` IS NULL AND `asID` NOT IN "
                         f"(SELECT `asID` FROM `{self.__data_name}`)")
                cursor.execute(query)
                self.connection.commit()
                # remove ads from input already in ads table
                query = f"DELETE FROM `{self.__data_name}` WHERE `asID` IN (SELECT `asID` FROM `{self.__data_name}`)"
                cursor.execute(query)
                self.connection.commit()
                # insert input table records in case of new ads
                query = (f"INSERT INTO `ads` (`asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, `Engine`, "
                         f"`Seller`, `Country`, `Address`, `Link`, `Color`, `PriceEuro`, `MileageKm`, `Start_Date`) "
                         f"SELECT `asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, `Engine`, `Seller`, "
                         f"`Country`, `Address`, `Link`, `Color`, `PriceEuro`, `MileageKm`, `Start_Date` "
                         f"FROM `{self.__data_name}`")
                cursor.execute(query)
                self.connection.commit()
                # delete input table
                query = f"DROP TABLE  `{self.__data_name}`"
                cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            print(query)
            print(f"Error: {e}")

    def update(self, subject: ReaderPublisher) -> None:
        self.__data_set = subject.get_result()
        print(self.__data_set)

    def update_db(self, name: str, results: dict) -> None:
        self.__data_name = "import_" + name
        self.__data_date = name[0:4] + '-' + name[4:6] + '-' + name[6:8]
        self.__data_set = results
        self.__do_update()
