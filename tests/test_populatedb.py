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


