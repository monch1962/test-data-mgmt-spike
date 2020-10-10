#!/usr/bin/env python3

#from sqlalchemy import Table, MetaData, Column, Integer
import sqlalchemy as db
import sys

class DataLoader:
    def __init__(self, datamapfile):
        self.datamapfile = datamapfile

    def read_datamap(self):
        import yaml
        with open(self.datamapfile) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.data = data
            self.dburl = data['dburi']
            return data
    
    def validate_datamap(self):
        engine = db.create_engine(self.data['dburi'])
        print(self.data)
        with engine.connect() as connection:
            for d in self.data['datafilemaps']:
                self._validate_table_exists(engine, d['table'])
                print(d['fieldmaps'])
                for k in d['fieldmaps']:
                    print(k)
                    self._validate_field_exists(engine, d['table'], k)

    def _validate_table_exists(self, engine, tablename):
        print("Checking existence of table '%s'" % tablename)
        if not engine.dialect.has_table(engine, tablename):
            print("Table '%s' not in database...exiting without updating data" % tablename)
            return False
        else:
            print("Table '%s' found" % tablename)
        return True

    def _validate_field_exists(self, engine, tablename, fieldname):
        print("Checking if field '%s' exists in table '%s'" % (fieldname, tablename))
        with engine.connect() as connection:
            try:
                rows = connection.execute("SELECT %s FROM %s LIMIT 1;" % (fieldname, tablename))
            except:
                print("Field '%s' not found in table '%s'...exiting" % (fieldname, tablename))
                return False
        return True
    
    def create_table_if_not_exists(self):
        pass

if __name__ == '__main__':
    dl = DataLoader('datamap.yaml')
    datamap = dl.read_datamap()
    print(datamap)
    dl.validate_datamap()
    engine = db.create_engine(dl.dburl)
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
