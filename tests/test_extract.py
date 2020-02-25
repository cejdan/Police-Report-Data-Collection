import sys
import pytest
import re
import tempfile
from io import BytesIO

sys.path.insert(1, '../project0')

from project0 import project0

def test_extraction():
    
    with open("../docs/testIncident.pdf", mode = 'rb') as f:
        myDoc = f.read()
        
    PDF_list = []
    PDF_list.append(myDoc)
    extractResults = project0.extractincidents(PDF_list)
    #Here we want to test a few things about our output.
    #First, it is a string.
    assert type(extractResults) == str
    #Next, it has the right shape (no more than 5 items in a line)
    #We can achieve this with a regex search. If the search returns nothing, then we are good.
    sixColumns = re.compile(r".+,.+,.+,.+,.+,")
    #fourColumns = re.compile(r".+,.+,.+,(.+)?[^,]\n)
    assert sixColumns.match(extractResults == None)
    #fourOrLessColumns = re.compile(r".+,\n)