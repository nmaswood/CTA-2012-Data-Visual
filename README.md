# CTA-2012-Data-Visual

This project aggregates information about October 2012 bus ridership data 
and displays it via the Google Maps API


## Look in D3 for a Bubble Chart of the information
## Look in Gmaps for a mapping of the information


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
