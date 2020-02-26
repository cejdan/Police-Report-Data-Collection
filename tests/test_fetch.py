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
    good_url2 = "http://normanpd.normanok.gov/filebrowser_download/657/2020-02-24%20Daily%20Incident%20Summary.pdf"
    fetchResults = project0.fetchincidents(good_url)
    fetchResults2 = project0.fetchincidents(good_url2)
    #We want to check that if we give a valid url, we return a list of length 1
    #That list contains our PDF file. The reason it is a list is because the code
    #Can actually handle all 7 PDFs on the website at once, if desired.
    assert type(fetchResults) == list
    assert len(fetchResults) == 1
    assert type(fetchResults2) == list
    assert len(fetchResults2) == 1


def test_fetch_bad_url():
    bad_url = "http://youtube.com"
    with pytest.raises(NameError):
        project0.fetchincidents(bad_url)




