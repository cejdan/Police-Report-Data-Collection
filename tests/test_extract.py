import sys
import pytest
import re
import tempfile
import os


#If you are running the program from the cs5293sp20-project0 folder we need:
myPath = os.path.abspath("../cs5293sp20-project0/project0")
sys.path.insert(1, myPath)

#If you are running the program from the tests folder, we need:
myPath = os.path.abspath("../project0")
sys.path.insert(1, myPath)

from project0 import project0

def test_extraction():
    
    currentDir = os.getcwd()
    if(os.path.basename(currentDir) == "cs5293sp20-project0"):
        docPath = os.path.abspath("docs/testIncident.pdf")
    elif(os.path.basename(currentDir) == "tests"):
        docPath = os.path.abspath("../docs/testIncident.pdf")

    with open(docPath, mode = 'rb') as f:
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
    assert sixColumns.match(extractResults) == None
