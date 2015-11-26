from csv import reader
import sqlite3 as sql

class populate_table(object):

	def __init__(self,db_name,table_name):
		self.db_name = db_name
		self.table_name = table_name
		self.start = self.start_queries()

	def start_queries(self):

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
		 	(?, ?, ?, ?, ?,?,?,?)""" % self.table_name,

		"CREATE" : '''CREATE TABLE %s(
		stop_id  		INT PRIMARY KEY NOT NULL,
       	on_street		VARCHAR(50),
		cross_street 	VARCHAR(30),
       	routes       	VARCHAR(10),
       	boardings    	FLOAT,
		alightings		FLOAT,
		latitude		DECIMAL,
		longitude		DECIMAL
		);''' % self.table_name}
		

	def initialize_table(self):
		connection = sql.connect(self.db_name)
		cursor = connection.cursor()

		try:
			connection.execute(self.start["CREATE"])

		except sql.Error as e:
			print "intialize-table: The following error occured %s" % e

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
		
		connection.commit()
		connection.close()

	def view_table(self):
		try:
			connection = sql.connect(self.db_name)
			cursor = connection.cursor()
			rows = cursor.execute("""SELECT * FROM %s""" % self.table_name)
			print 'stop_id,on_street,cross_street,routes,boardings,alightings,latitude,longitude'
			for row in rows:
				print row

		except sql.Error as e:
			print "Something wrong happened %s" % e





populate_table = populate_table(db_name="bus_data.db",table_name="CTA1012")

populate_table.initialize_table()


populate_table.view_table()


#find the longest bus route by number of stops
#and the bus stop that appears on the most bus routes.
