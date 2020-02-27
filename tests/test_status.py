import sys
import pytest
import os
 
#If you are running the program from the cs5293sp20-project0 folder we need:
myPath = os.path.abspath("../cs5293sp20-project0/project0")
sys.path.insert(1, myPath)

#If you are running the program from the tests folder, we need:
myPath = os.path.abspath("../project0")
sys.path.insert(1, myPath)


from project0 import project0

def test_status():

    currentDir = os.getcwd()
    #We are using a pre-populated database for this test, located in the docs folder.
    #We need to navigate to it and set the absolute path as dbpath
    if(os.path.basename(currentDir) == "cs5293sp20-project0"):
        dbPath = os.path.abspath("../cs5293sp20-project0/docs/populated.db")
    elif(os.path.basename(currentDir) == "tests"):
        dbPath = os.path.abspath("../docs/populated.db")
    
    myRows = project0.status(dbPath)
    #Let's check to make sure the output is of the correct type(s). If not, we know we have a problem.
    assert type(myRows) == list
    assert type(myRows[0]) == tuple
    assert type(myRows[0][0]) == str
    assert type(myRows[0][1]) == int
