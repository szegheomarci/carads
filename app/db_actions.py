import pymysql
import re


# format date from mm/YYYY to YYYY-mm-15
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


# Example: currency_to_int('€ 3,900,000.-') => 3900000
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


class DatabaseLoader:
    def __init__(self, host, port, user, password, db):
        # Connect to the database (replace these values with your database credentials)
        self.connection = pymysql.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_import_table(self, table_name, start_date):
        cursor = self.connection.cursor()
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
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
        `Start_Date` DATE DEFAULT '{start_date}'
        )
        '''

        try:
            cursor.execute(create_table_query)
        except Exception as e:
            print(f"Error: {e}")

        self.connection.commit()
        self.connection.close()

    def insert_list(self, table_name, records):
        self.connection.ping()
        try:
            with self.connection.cursor() as cursor:
                # Build the SQL query with placeholders for values
                query = f"INSERT INTO {table_name} (`asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, "
                query += ("`Engine`, `Seller`, `Country`, `Address`, `Link`, `Color`,  `PriceEuro`, `MileageKm`) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                # Iterate through the list of records and execute the query for each record
                for record in records:
                    # Extract values from the dictionary
                    asid = record.get('id')
                    title = record.get('title')
                    subtitle = record.get('subtitle')
                    price = record.get('price')
                    odo = record.get('odo')
                    manufdate = format_date(record.get('proddate'))
                    engine = record.get('engine')
                    dealer = record.get('dealer')
                    country = record.get('country')
                    zip = record.get('zip')
                    link = record.get('link')
                    color = extract_color(record.get('link'), record.get('id'))
                    priceeuro = unit_to_int(record.get('price'))
                    mileagekm = unit_to_int(record.get('odo'))

                    print(query, (asid, title, subtitle, price, odo, manufdate, engine, dealer, country, zip, link, color, priceeuro, mileagekm))

                    # Execute the query with the record values as parameters
                    cursor.execute(query, (asid, title, subtitle, price, odo, manufdate, engine, dealer, country, zip, link, color, priceeuro, mileagekm))
                    # Commit the changes to the database
                    self.connection.commit()

        except Exception as e:
            print(f"Error: {e}")
        #finally:
            # Close the database connection
            #self.connection.close()
