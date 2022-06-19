# databaseLib
poorly made library for using psql databases in python
I made it because I found myself rewriting code a lot when working with psql so I compiled a bunch of the most commond stuff into one library

# commands

databaseLib(dbname: str, dbuser: str, dbpass: str, dbhost: str, dbport: str) -
  constructor method that sets up the lib for use, if you've somehow found yourself using this lib you should know what the name, user, password, host and port are.

getTables() -
  returns an array of every table in the database.

getTable(tableName: str) -
  returns an entire table.
  
makeTable(tableName: str, params: list()) -
  makes a new table and commits the change to the database.
  The params argument is a 2d array that contains the table params.
  The array should be formatted as [[SQLDATATYPE, "TABLENAME"]].
  An example of a valid params array would be [[INT, "id"], [TEXT, "name"]].

deleteTable(tableName: str) -
  deletes the table that its given and commits changes to the database.
 
 formatTable(tableName: str) -
  returns a table formatted using the tabulate library, this method is purely cosmetic.
 
execute(command: str) -
  allows the user to execute normal psql commands, pretty redundant.
  
getFreq(tableName: str, columnName: str) -
    returns how often each entry occurs in a given column.
 
getWholeDB() - returns a whole database in the form of the standard psql array.

getColumns(tableName: str) - returns the name of every column in a given table.

getColumn(talbeName: str, columnName: str) - returns every entry within a given column from a given table.

searchColumn(tableName: str, columnName: str, searchTerm: str) - indexs a column from a table and returns all results.

searchTable(tableName: str, searchTerm: str) - indexs a whole table and returns all results.
