import sys
import pytest
 
sys.path.insert(1, '/home/ncejda/gitProjects/Police-Incident-Reports/project0')



from project0 import project0 as proj


def test_fetch_good_url():
    good_url = "http://normanpd.normanok.gov/content/daily-activity"
    fetchResults = proj.fetchincidents(good_url) 
    assert type(fetchResults) == list
    assert len(fetchResults) == 1


def test_fetch_bad_url():
    bad_url = "http://youtube.com"
    with pytest.raises(NameError):
        proj.fetchincidents(bad_url)




