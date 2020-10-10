#import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
import test_data_loader

def test_nothing():
    assert 1 == 1

#def test_load_class():
#    dl = TestDataLoader()