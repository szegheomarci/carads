# DB-Loader
DB Loader reads the collected ads from the configured input source and imports them into the ads database.
The ads table is updated:
* the new ads are added
* ads that do not have an end date, but are not in the new set, get their end date
* ads that already had an end date but appear in the new set, get their end dates cleared

## Configuration
Place the configuration in the file `config/config.yaml`. Source can be file or Kafka topic.

### Input
If **file** is configured, place the file(s) in the `input` folder. File format is either json or delimiter separated values.
In case of delimiter separated values, define the delimiter.  
_Example_:
```yaml
source:
  type: file
  format: dsv
  delimiter: "####"
```
```yaml
source:
  type: file
  format: json
```
If **Kafka** topic is configured, describe the consumer parameters in the config file.

### Database
The ads are uploaded to a MySQL database. For initializing the database, see https://github.com/szegheomarci/db-mysql.
Declare the MySQL access in the `config.yaml`.  
_Example_:
```yaml
database:
  host: 192.168.0.100
  port: 3306
  user: myuser
  password: mypass
  database: db
```
