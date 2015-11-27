from csv import reader
import sqlite3 as sql
from collections import defaultdict


# Load data loads the intial data from the CSV
# into a sql table. The table is called CTA1012

# load_data takes optional parameters of a database name and a table name

###USAGE###

#load_data = load_data()
#load_data.view()

###########

# Aggregate data sums the data on basis
# of stop and route. The tables are called
# stopagg and route agg respectively.

# aggregate_data takes optional parameters of a database name and a table name

###USAGE###

#aggregate_data = aggregate_data()
#aggregate_data.initialize("ROUTE")
#aggregate_data.intialize("STOP")
#aggregate_data.view()

###########


class load_data(object):

	def __init__(self,db_name="bus_data.db",table_name="CTA1012"):
		self.db_name = db_name
		self.table_name = table_name
		self.start = self.queries()

	def queries(self):

		return {
		"INSERT" : """INSERT INTO %s(
			stop_id,
			on_street,
		 	cross_street,
		 	routes,
		 	boardings,
		 	alightings,
		 	latitude,
		 	longitude)  VALUES
		 	(?, ?, ?, ?, ?,?,?,?)
		 	""" % self.table_name,

		"CREATE" : '''CREATE TABLE %s(
			stop_id  		INT PRIMARY KEY NOT NULL,
       		on_street		VARCHAR(50),
			cross_street 	VARCHAR(30),
       		routes       	VARCHAR(10),
       		boardings    	FLOAT,
			alightings		FLOAT,
			latitude		DECIMAL,
			longitude		DECIMAL);
			''' % self.table_name,
		"SELECT" : """SELECT * FROM %s""" % self.table_name}
		

	def initialize(self):
		connection = sql.connect(self.db_name)
		cursor = connection.cursor()

		try:
			connection.execute(self.start["CREATE"])
			with open( str(self.table_name) + '.csv') as csv:
				data = reader(csv, delimiter=',', quotechar='"')
				next(data)
				for row in data:
					stop_id, on_street, cross_street, routes, boardings, alightings, month_beginning, daytype, location = row
					latitude, longitude = location.strip('()').split(",")
					try:
						connection.execute(self.start["INSERT"], (stop_id,on_street,cross_street,routes,boardings,alightings,latitude,longitude));
					except sql.Error as e:
						print "initialize-table: The following error occured %s" % e
						break
		except sql.Error as e:
			print "intialize-table: The following error occured %s" % e

		connection.commit()
		connection.close()

	def view(self):
		try:
			connection = sql.connect(self.db_name)
			cursor = connection.cursor()
			rows = cursor.execute(self.start["SELECT"])
			print 'stop_id,on_street,cross_street,routes,boardings,alightings,latitude,longitude'
			for row in rows:
				print row

		except sql.Error as e:
			print "Something wrong happened %s" % e

class aggregate_data(object):

	def __init__(self,db_name="bus_data.db",table_name="CTA1012"):
		self.db_name = db_name
		self.table_name = table_name
		self.agg = self.queries()

	def queries(self):
		return {

		"CREATEROUTE" : """CREATE TABLE routeagg(
			route varchar(10),
			route_count int,
			sum_alight FLOAT,
			avg_alight FLOAT,
			sum_board FLOAT,
			avg_board FLOAT);
		 """,

		 "INSERTROUTE": """INSERT INTO routeagg(
		 	route,
		 	route_count,
		 	sum_alight,
		 	avg_alight,
		 	sum_board,
		 	avg_board) VALUES (
		 	?,?,?,?,?,?)""",

		"ROUTE" :  """SELECT 
			routes,
			COUNT(routes),
		 	SUM(alightings),
		 	AVG(alightings),
		 	SUM(boardings),
		 	AVG(boardings)
		 FROM %s GROUP BY routes ORDER BY routes DESC
		 """ % self.table_name,

		 "CREATESTOP" : """CREATE TABLE stopagg(
			on_street varchar(50),
			stop_count int,
			sum_alight FLOAT,
			avg_alight FLOAT,
			sum_board FLOAT,
			avg_board FLOAT);
		 """,

		 "INSERTSTOP": """INSERT INTO stopagg(
		 	on_street,
		 	stop_count,
		 	sum_alight,
		 	avg_alight,
		 	sum_board,
		 	avg_board) VALUES(
		 	?,?,?,?,?,?)""",

		 "STOP" : """ SELECT 
		 	on_street,
		 	COUNT(on_street),
		 	SUM(alightings),
		 	AVG(alightings),
		 	SUM(boardings),
		 	AVG(boardings)
			FROM %s GROUP BY on_street ORDER BY on_street
			""" % self.table_name,
		} 

	def initialize(self,query):

		connection = sql.connect(self.db_name)
		cursor1 = connection.cursor()
		cursor2 = connection.cursor()
		try:
			cursor2.execute(self.agg["CREATE" + query])
			data = cursor1.execute(self.agg[query])
			for line in data:
				cursor2.execute(self.agg["INSERT" + query], line)
			connection.commit()

		except sql.Error as e:
			print e
	def view(self,type):
		try:
			connection = sql.connect(self.db_name)
			cursor = connection.cursor()

			tables = {"ROUTE": "routeagg", "STOP":"stopagg"}

			select = " SELECT * FROM %s"  % tables[type]

			rows = cursor.execute(select)
			print type, "count" + type, "sum alightings", "avg alightings", "sum boardings", "avg boardings"
			for row in rows:
				print row

		except sql.Error as e:
			print "Something wrong happened %s" % e



