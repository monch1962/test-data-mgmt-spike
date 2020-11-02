#!/usr/bin/env python3
"""
This program includes the TestDataLoader class, plus a small code fragment to
demonstrate how to use the class
"""

#from sqlalchemy import Table, MetaData, Column, Integer
#import os, json
import os
import sys
import sqlalchemy as db
import yaml

class TestDataLoader:
    """
    TestDataLoader is a class designed to populate test data into databases. As it
    uses SQLAlchemy under the covers, it should be portable to many different types
    of databases (e.g. sqlite, Postgres, MySQL, MS SQL)
    """
    def __init__(self, datamapfile):
        self.datamapfile = datamapfile
        self._read_datamap()

    def _read_datamap(self):
        #import yaml
        with open(self.datamapfile) as datamap_file:
            data = yaml.load(datamap_file, Loader=yaml.FullLoader)
            self.data = data
            self.dburl = data['dburi']
        self.engine = db.create_engine(self.data['dburi'])

    def validate_datamap(self):
        """
        Validate the content of the datamap against the database
        """
        print(self.data)
        #with self.engine.connect() as connection:
        for data_file_map in self.data['datafilemaps']:
            if not self._validate_table_exists(data_file_map['table']):
                return False
            for field_map in data_file_map['fieldmaps']:
                for k in field_map:
                    if not self._validate_field_exists(data_file_map['table'], k):
                        return False
        return True

    def _validate_table_exists(self, tablename):
        """
        Validate that the given tablename exists in the database
        """
        print("Checking existence of table '%s'" % tablename)
        if not self.engine.dialect.has_table(self.engine, tablename):
            print("Table '%s' not in database...exiting without updating data" % tablename)
            return False
        print("Table '%s' found" % tablename)
        return True

    def _validate_field_exists(self, tablename, fieldname):
        """
        Validate that the given fieldname exists in the given tablename
        """
        print("Checking if field '%s' exists in table '%s'" % (fieldname, tablename))
        with self.engine.connect() as connection:
            try:
                connection.execute("SELECT %s FROM %s LIMIT 1;" % (fieldname, tablename))
            except:
                print("Field '%s' not found in table '%s'...exiting" % (fieldname, tablename))
                return False
        return True

    def upsert_data(self):
        """
        Insert or update data from the data file into the appropriate database tables
        """
        print("About to upsert data")
        with self.engine.connect() as connection:
            for df_map in self.data['datafilemaps']:
                db_table = df_map['table']
                db_datafile = df_map['datafile']
                print("Populating table '%s' from file '%s'" % (db_table, db_datafile))
                for field_map in df_map['fieldmaps']:
                    print('field_map: %s' % field_map)
                    for field in field_map:
                        print('field: %s' % field)

    def _upsert_record(self, tablename, record):
        pass

    def truncate_table(self, tablename):
        """
        Remove all rows from the specified table
        """
        print("Truncating table '%s'" % tablename)
        with self.engine.connect() as connection:
            connection.execute("DELETE FROM %s" % tablename)

    def list_tables(self):
        """
        Return the SQLAlchemy details for all tables in the database
        """
        meta = db.MetaData()
        meta.reflect(bind=self.engine)
        return meta.tables

if __name__ == '__main__':
    datamap = os.environ.get("DATAMAP")
    if datamap is None:
        NO_DATAMAP = """
        Error:
        you need environment variable DATAMAP to point to your datamap YAML file
        """
        print(NO_DATAMAP, file=sys.stderr)
        sys.exit(1)
    #dl = TestDataLoader('datamap.yaml')
    data_loader = TestDataLoader(datamap)
    data_loader.validate_datamap()
    data_loader.upsert_data()
    data_loader.truncate_table('mytable')
    print("database table names: %s" % data_loader.list_tables().keys())
    print("database table info: %s" % data_loader.list_tables())

    engine = db.create_engine(data_loader.data['dburi'])
    if not engine.dialect.has_table(engine, "usertable"):  # If table don't exist, Create.
        metadata = db.MetaData(engine)
        # Create a table with the appropriate Columns
        db.Table("usertable", metadata,
            db.Column('Id', db.Integer, primary_key=True, nullable=False),
            db.Column('firstname', db.String), db.Column('lastname', db.String),
            db.Column('street', db.String), db.Column('suburb', db.String),
            db.Column('postcode', db.Integer), db.Column('state', db.String),
            db.Column('country', db.String), db.Column('email', db.String),
            db.Column('phone', db.String)
        )
        # Implement the creation
        metadata.create_all()
