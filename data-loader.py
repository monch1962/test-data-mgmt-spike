#!/usr/bin/env python3

#from sqlalchemy import Table, MetaData, Column, Integer
import sqlalchemy as db
import os, json

class DataLoader:
    def __init__(self, datamapfile):
        self.datamapfile = datamapfile
        self._read_datamap()

    def _read_datamap(self):
        import yaml
        with open(self.datamapfile) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.data = data
            self.dburl = data['dburi']
        self.engine = db.create_engine(self.data['dburi'])
    
    def validate_datamap(self):
        print(self.data)
        with self.engine.connect() as connection:
            for d in self.data['datafilemaps']:
                if not self._validate_table_exists(d['table']):
                    return False
                for fm in d['fieldmaps']:
                    for k in fm:
                        if not self._validate_field_exists(d['table'], k):
                            return False

    def _validate_table_exists(self, tablename):
        print("Checking existence of table '%s'" % tablename)
        if not self.engine.dialect.has_table(self.engine, tablename):
            print("Table '%s' not in database...exiting without updating data" % tablename)
            return False
        else:
            print("Table '%s' found" % tablename)
        return True

    def _validate_field_exists(self, tablename, fieldname):
        print("Checking if field '%s' exists in table '%s'" % (fieldname, tablename))
        with self.engine.connect() as connection:
            try:
                rows = connection.execute("SELECT %s FROM %s LIMIT 1;" % (fieldname, tablename))
            except:
                print("Field '%s' not found in table '%s'...exiting" % (fieldname, tablename))
                return False
        return True
    
    def upsert_data(self):
        print("About to upsert data")
        with self.engine.connect() as connection:
            for dfm in self.data['datafilemaps']:
                t = dfm['table']
                df = dfm['datafile']
                print("Populating table '%s' from file '%s'" % (t, df))
                for fm in dfm['fieldmaps']:
                    print('fm: %s' % fm)
                    for f in fm:
                        print('f: %s' % f)

    def _upsert_record(self, tablename, record):
        pass

    def truncate_table(self, tablename):
        print("Truncating table '%s'" % tablename)
        with self.engine.connect() as connection:
            connection.execute("DELETE FROM %s" % tablename)

if __name__ == '__main__':
    dl = DataLoader('datamap.yaml')
    dl.validate_datamap()
    dl.upsert_data()
    dl.truncate_table('mytable')

    engine = db.create_engine(dl.dburl)
    #engine = db.create_engine(dl.data['dburl'])
    with engine.connect() as connection:
        result = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #print(result)
        for row in result:
            print(row)
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
