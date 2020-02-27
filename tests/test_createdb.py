import sys
import pytest
import os
import sqlite3
 
#If you are running the program from the cs5293sp20-project0 folder we need:
myPath = os.path.abspath("../cs5293sp20-project0/project0")
sys.path.insert(1, myPath)

#If you are running the program from the tests folder, we need:
myPath = os.path.abspath("../project0")
sys.path.insert(1, myPath)


from project0 import project0

def test_creatdb():
    #This test will create a normanpd database, and check that all the column names are correct
    
    #First we establish a path to our normanpd.db file (created in the project0 folder)
    currentDir = os.getcwd()
    
    if(os.path.basename(currentDir) == "cs5293sp20-project0"):
        dbPath = os.path.abspath("../cs5293sp20-project0/project0/normanpd.db")
    elif(os.path.basename(currentDir) == "tests"):
        dbPath = os.path.abspath("../project0/normanpd.db")
    
    #Then we create a normanpd database
    project0.createdb()
    
    #We re-open a connection to the sqlite3 database, and run a PRAGMA table_info() statement
    conn = sqlite3.connect(dbPath)
    results = conn.execute("PRAGMA table_info(incidents);")
    output = results.fetchall()
    
    #Now we can check if the column names match the expected output.
    assert output[0][1] == 'Date / Time'
    assert output[1][1] == 'Incident Number'
    assert output[2][1] == 'Location'
    assert output[3][1] == 'Nature'
    assert output[4][1] == 'Incident Ori'
    
    #Finally we close the connection to the database
    conn.close()



    