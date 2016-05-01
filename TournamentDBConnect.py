import psycopg2

class TournamentDB:
	_db_connection = None
	_db_cursor = None

	def __init__(self, dbname):
		self._db_connection = psycopg2.connect("dbname=tournament")
		self._db_cursor = self._db_connection.cursor();

	def __del__(self):
		self._db_connection.close();

 	def selectquery(self, query):
 		self._db_cursor.execute(query)
 		return self._db_cursor.fetchall();

	def query(self, query, parameter):
		self._db_cursor.execute(query, parameter)
 		#print(self._db_cursor.statusmessage)
		self._db_connection.commit();

	def fetchonequery(self, query):
 		self._db_cursor.execute(query)
 		return self._db_cursor.fetchone();
	
