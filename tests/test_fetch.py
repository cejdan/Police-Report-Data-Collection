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


def test_fetch_good_url():
    good_url = "http://normanpd.normanok.gov/content/daily-activity"
    fetchResults = project0.fetchincidents(good_url) 
    assert type(fetchResults) == list
    assert len(fetchResults) == 1


def test_fetch_bad_url():
    bad_url = "http://youtube.com"
    with pytest.raises(NameError):
        project0.fetchincidents(bad_url)




