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

def test_populatedb():
    
    currentDir = os.getcwd()
    if(os.path.basename(currentDir) == "cs5293sp20-project0"):
        dbPath = os.path.abspath("../cs5293sp20-project0/project0/normanpd.db")
        csvPath = os.path.abspath("../cs5293sp20-project0/docs/incidentsTest.csv")
    elif(os.path.basename(currentDir) == "tests"):
        dbPath = os.path.abspath("../project0/normanpd.db")
        csvPath = os.path.abspath("../docs/incidentsTest.csv")
        
    project0.createdb()
    project0.populatedb(dbPath, csvPath)
    
    #We need to check if our db was populated properly now
    conn = sqlite3.connect(dbPath)
    results = conn.execute("SELECT Nature FROM incidents WHERE Nature = 'Traffic Stop'")
    output = results.fetchall()
    conn.close()
    #We pretty much know for sure that all the incident PDFs will have at least 1 Traffic Stop.
    #It's a good check to ensure our database is being properly populated for that reason.
    assert len(output) > 1


