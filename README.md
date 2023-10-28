# DB-Loader
DB Loader reads the collected ads from the configured input source and imports them into the ads database.
The ads table is updated:
* the new ads are added
* ads that were previously active, but no longer in the file get the end date

## Configuration
