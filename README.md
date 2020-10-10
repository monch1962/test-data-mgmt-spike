[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/monch1962/test-data-mgmt-spike)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![pylint](https://raw.githubusercontent.com/monch1962/test-data-mgmt-spike/main/pylint-badge.svg)](https://github.com/monch1962/test-data-mgmt-spike)

# test-data-mgmt-spike
Spike to try out some ideas with Test Data Management.

This tool is based around Python's SQLAlchemy library, in an attempt to work with just about any database product (e.g. SQLite, MySQL, Postgres, MS SQL, AWS DynamoDB) that I'm likely to encounter. If different databases appear, there's a very good chance they will be supported by SQLAlchemy fairly quickly, so supporting them should simply be a matter of `pip install`ing the appropriate database driver.

...Or so I hope.

### High level approach
- generate a set of test data, using the `http://generatedata.com` toolset. The generated data should be saved as JSON format, with one JSON file for each database table to be populated
- create a YAML file to map the JSON files to the database/tables/fields you wish to populate
- create a small script around the `TestDataManagement` class in the `data_loader.py` file to populate your test data into the database. An example of how to use the `TestDataManagement` class is included at the bottom of `data_loader.py`, and should be adapted to suit your needs

## Data generation

Data is generated using the http://generatedata.com tool. This is an open-source tool that supports a range of different data types, can be extended, and has a Dockerfile to make it easily hosted inside test infrastructure.

One possible use case would be to include a generatedata.com Docker container *inside* your test environment, then create & store common test data definitions inside the generatedata instance so you can quickly retrieve them & generate new data on demand.

Use this tool to generate data for the table/s you wish to populate, then save these files as JSON. A sample file is under `./generated-data` in this repository

## Data Mapping

The `datamap.yaml` file in this repository contains a sample for mapping generated data files to the database, tables & fields you wish to update

## To Use

`$ ./data_loader.py` should run as a sample to update the `generated-data/database.db` SQLite database.

## To update PyLint badge

After making code changes, but before committing and pushing to github

`$ pylint-badge data_loader.py pylint-badge.svg`