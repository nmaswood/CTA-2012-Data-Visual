# CTA-2012-Data-Visual

This project aggregates information about October 2012 bus ridership data 
and displays it via the Google Maps API


#### Look in D3 for a Bubble Chart of the information
#### Look in Gmaps for a mapping of the information


## Data Schema from CSV

| column        | data_type           |
| :-------------: |:-------------:| 
| stop_id    | INT PRIMARY KEY NOT NULL | 
| on_street      | VARCHAR(50)      |  
| cross_street | VARCHAR(30)      |
| routes | VARCHAR(30)     |
| boardings | VARCHAR(10)     |
| alightings| FLOAT      |
| latitude| FLOAT      |
| longitude | DECIMAL     |


## Data Aggregate Schema 

| column        | data_type           |
| :-------------: |:-------------:| 
| route | VARCHAR(10)     |
| route_count | int       |
| sum_alight | FLOAT     |
| avg_alight| FLOAT      |
| sum_board| FLOAT      |
| avg_board | FLOAT     |


| column        | data_type           |
| :-------------: |:-------------:| 
| on_street | VARCHAR(50)     |
| stop_count | int       |
| sum_alight | FLOAT     |
| avg_alight| FLOAT      |
| sum_board| FLOAT      |
| avg_board | FLOAT     |


### Load Data 

Load data loads the intial data from the CSV
into a sql table. The table is called CTA1012

load_data takes optional parameters of a database name and a table name

####USAGE

load_data = load_data()
load_data.initialize()
load_data.view()

aggregate_data takes optional parameters of a database name and a table name

aggregate_data = aggregate_data()
aggregate_data.initialize("ROUTE")
aggregate_data.initialize("ON_STREET")
aggregate_data.view('ROUTE', order=True)
aggregate_data.view('ON_STREET', order=True)



#### References

This project uses code from 

http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python

This uses code from http://bl.ocks.org/mbostock/4063269




