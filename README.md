# CTA-2012-Data-Visual

This project aggregates information about October 2012 bus ridership data 
and displays it via the Google Maps API



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


### Basic Visual

Returns a heat map where higher density
refers bus stops that appear more frequently


### Verbose Visual

A marker map where the darker the marker
the higher the value for the specified metric.

A user can click on a marker and
see the statisitics associated with it

##Usage

### populate_data


Input:  a csv for Chicago bus data for a particular year and month
Output: A sql database containing table of data

Input : A sql database containing table of  bus data
Output: A table grouping aggregates of the data by on_street and by route

### visualize_data


See comments of visualize_data.py

