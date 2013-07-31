import MyYogi
from nose import tools
import model

def test_get_asana():
    ''' tests if returns correct query result'''
    result = MyYogi.get_asana("mountain")
    tools.assert_equals(result,"mountain")

def test_coin_toss():
    '''tests if coin_toss returns a decimal between 0 and 1'''
    result = 