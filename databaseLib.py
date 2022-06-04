import os
import psycopg2
import sys
from tabulate import tabulate;

class main:

	def getTables(self):
		c = self.conn.cursor();
		c.execute("""SELECT
		    table_schema || '.' || table_name
		FROM
		    information_schema.tables
		WHERE
		    table_type = 'BASE TABLE'
		AND
		    table_schema NOT IN ('pg_catalog', 'information_schema');
		""");
		items = c.fetchall();
		return [i[0] for i in items];

	def execute(self, command: str):
		c = self.conn.cursor()
		c.execute(command);
		items = c.fetchall();
		items = self.__fixTable(items);
		self.conn.commit();
		return items;

	def getTable(self, tableName: str):
		c = self.conn.cursor();
		try:
			c.execute(f"SELECT * FROM {tableName}");
			items = c.fetchall();
			items = self.__fixTable(items);
			return items;
		except Exception as e:
			print("unable to process. You may have typed in the table name incorrectly, use getTables() to get a full list of all tables in the database");
			print();
			print(e);
			return;

	def makeTable(self, tableName: str, params: []):
		c = self.conn.cursor();
		try:
			c.execute(f"""CREATE TABLE {tableName} (
				{self.__formatList(params)}
			)""");
			self.conn.commit();
			print(f"created table {tableName}");
		except Exception as e:
			print("unable to make table");
			print(e);

	def deleteTable(self, tableName: str):
		c = self.conn.cursor();
		try:
			c.execute(f"DROP TABLE {tableName}");
			print(f"removed table {tableName}");
			self.conn.commit();
			return
		except Exception as e:
			print("unable to remove table");
			print("use the command getTables() to get all tables in the database");
			print(e);

	def formatTable(self, tableName: str):
		table = self.getTable(tableName);
		c = self.conn.cursor();
		try:
			c.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tableName}'");
		except Exception as e:
			print("unable to handle request");
			print("to print a list of all tables use getTables()");
			print(e);
		columns = c.fetchall();
		headers = [];
		for i in range(len(columns)):
			headers.append(columns[i][0]);
		print(tabulate(
			table,
			headers = headers,
			tablefmt = 'psql'
		))

	def getFreq(self, tableName: str, columnName: str):
		c = self.conn.cursor();
		try:
			c.execute(f"SELECT {columnName} FROM {tableName}");
			items = c.fetchall();
			items = self.__fixTable(items);
		except Exception as e:
			print("unable to handle request");
			print();
			print(e);
			return;

		freq = {}
		for i in items:
			if i[0] in freq:
				freq[i[0]] += 1;
			else:
				freq[i[0]] = 1;

		names = [[x, y] for x, y in freq.items()];

		names.sort(key = lambda row: (row[1]), reverse=True);

		return names;

	def getWholeDB(self):
		whole = [];
		c = self.conn.cursor();
		for table in self.getTables():
			c.execute(f"SELECT * FROM {table[0]}")
			items = c.fetchall();
			whole.append(items);	

		return whole;

	def formatArray(self, arr: [], headerArr: []):
		return tabulate(
			arr,
			headers = headerArr,
			tablefmt = 'psql'
			);

	def getColumns(self, tableName: str):
		ls = self.__formatColumns(tableName);
		return [i[0] for i in ls]

	def getColumn(self, tableName: str, columnName: str):
		c = self.conn.cursor();
		c.execute(f"SELECT {columnName} FROM {tableName}");
		items = c.fetchall();
		items = self.__fixTable(items);
		return [x[0] for x in items];

	def __formatColumns(self, tableName: str):
		c = self.conn.cursor();
		c.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tableName}'");
		return (c.fetchall());

	def __fixTable(self, items: []):
		del items[0];
		del items[-1];
		return items; 

	def __formatList(self, info: []):
		final = "";
		for i in range(len(info)-1):
			final += f"{info[i][0]} {info[i][1]},\n";
		final += f"{info[-1][0]} {info[-1][1]}";
		return final;

	def __init__(self, name: str):
		self.DB_NAME = f"{name}";
		DB_USER = "postgres"
		DB_PASS = "rootUser"
		DB_HOST = "localhost"
		DB_PORT = "5432"
		try:
		     self.conn = psycopg2.connect(database = self.DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
		     print("connected to database")
		except Exception as e:
		    print("unable to connect to Server")
		    print(e);
		    return;

