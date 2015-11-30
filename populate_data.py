from csv import reader
import sqlite3 as sql

# Load data loads the intial data from the CSV
# into a sql table. The table is called CTA1012

# load_data takes optional parameters of a database name and a table name

###USAGE###

#load_data = load_data()
#load_data.initialize()
#load_data.view()

###########


# aggregate_data takes optional parameters of a database name and a table name

#aggregate_data = aggregate_data()
#aggregate_data.initialize("ROUTE")
#aggregate_data.initialize("ON_STREET")
#aggregate_data.view('ROUTE', order=True)
#aggregate_data.view('ON_STREET', order=True)


###USAGE###

#aggregate_data = aggregate_data()
#aggregate_data.initialize("ROUTE")
#aggregate_data.intialize("STOP")
#aggregate_data.view('ROUTE', order=True)
#aggregate_data.view('STOP', order=True)

###########


class load_data(object):

	def __init__(self,db_name="bus_data.db",table_name="CTA1012"):
		self.db_name = db_name
		self.table_name = table_name
		self.start = self.queries()
		self.error = "{function}: The following error occured {error}"

	def queries(self):

		return {
		"INSERT" : """INSERT INTO {table_name}(
			stop_id,
			on_street,
		 	cross_street,
		 	route,
		 	boardings,
		 	alightings,
		 	latitude,
		 	longitude)  VALUES
		 	(?, ?, ?, ?, ?,?,?,?)
		 	""".format(table_name= self.table_name),

		"CREATE" : '''CREATE TABLE {table_name}(
			stop_id  		INT PRIMARY KEY NOT NULL,
       		on_street		VARCHAR(50),
			cross_street 	VARCHAR(30),
       		route       	VARCHAR(10),
       		boardings    	FLOAT,
			alightings		FLOAT,
			latitude		DECIMAL,
			longitude		DECIMAL);
			'''.format(table_name=self.table_name),

		"SELECT" : """SELECT * FROM {table_name}""".format(table_name =self.table_name)
		}
		

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
						connection.execute(self.start["INSERT"], (
							stop_id,
							on_street,
							cross_street,
							routes,
							boardings,
							alightings,
							latitude,
							longitude));
					except sql.Error as e:
						print self.error.format(function="initialize", error=e)
						break
		except sql.Error as e:
			print self.error.format(function="initialize", error=e)

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
			print self.error.format(function="view", error=e)

class aggregate_data(object):

	def __init__(self,db_name="bus_data.db",table_name="CTA1012"):
		self.db_name = db_name
		self.table_name = table_name
		self.agg = self.queries()
		self.error = "{function}: The following error occured {error}"


	def queries(self):
		return {

		"CREATE_ROUTE" : """CREATE TABLE ROUTE_AGG(
			route varchar(10),
			route_count int,
			sum_alight FLOAT,
			avg_alight FLOAT,
			sum_board FLOAT,
			avg_board FLOAT);
		 """,

		 "INSERT_ROUTE": """INSERT INTO ROUTE_AGG(
		 	route,
		 	route_count,
		 	sum_alight,
		 	avg_alight,
		 	sum_board,
		 	avg_board) VALUES (
		 	?,?,?,?,?,?)""",

		"ROUTE" :  """SELECT 
			route,
			COUNT(route),
		 	SUM(alightings),
		 	AVG(alightings),
		 	SUM(boardings),
		 	AVG(boardings)
		 FROM {table_name} GROUP BY route ORDER BY route 
		 """.format(table_name=self.table_name),

		 "CREATE_ON_STREET" : """CREATE TABLE ON_STREET_AGG(
			on_street varchar(50),
			on_street_count int,
			sum_alight FLOAT,
			avg_alight FLOAT,
			sum_board FLOAT,
			avg_board FLOAT);
		 """,

		 "INSERT_ON_STREET": """INSERT INTO ON_STREET_AGG(
		 	on_street,
		 	on_street_count,
		 	sum_alight,
		 	avg_alight,
		 	sum_board,
		 	avg_board) VALUES(
		 	?,?,?,?,?,?)""",

		 "ON_STREET" : """ SELECT 
		 	on_street,
		 	COUNT(on_street),
		 	SUM(alightings),
		 	AVG(alightings),
		 	SUM(boardings),
		 	AVG(boardings)
			FROM {table_name} GROUP BY on_street ORDER BY on_street
			""".format(table_name=self.table_name),
		} 

	def initialize(self,query):

		connection = sql.connect(self.db_name)
		cursor1 = connection.cursor()
		cursor2 = connection.cursor()
		try:
			cursor2.execute(self.agg["CREATE_" + query])
			data = cursor1.execute(self.agg[query])
			for line in data:
				cursor2.execute(self.agg["INSERT_" + query], line)
			connection.commit()

		except sql.Error as e:
			print self.error.format(function="initialize", error=e)

	def view(self,type,order=False):
		try:
			connection = sql.connect(self.db_name)
			cursor = connection.cursor()

			tables = {"ROUTE": "ROUTE_AGG", "ON_STREET":"ON_STREET_AGG"}

			select = " SELECT * FROM {table}".format(table=tables[type])
			if order:

				type_row = {"ROUTE":"route_count", "ON_STREET":"on_street_count"}

				select+= " ORDER BY {type_row}".format(type_row=type_row[type]) 

			rows = cursor.execute(select)
			print type, "count" + type, "sum alightings", "avg alightings", "sum boardings", "avg boardings"
			for row in rows:
				print row

		except sql.Error as e:
			print self.error.format(function="view", error=e)
