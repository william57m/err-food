"""Basic output validation tests"""

import re
import food

# pytest
extra_plugin_dir = '.'
pytest_plugins = ['errbot.backends.test']


def test_resto_pick(testbot):
    testbot.push_message('!resto pick')
    result = testbot.pop_message()
    assert result is not None
    restaurant = re.sub('I suggest ', '', result)
    assert restaurant in food.RESTAURANT_LIST

def test_resto_yelp(testbot):
    testbot.push_message('!resto yelp')
    result = testbot.pop_message()
    assert result is not None

def test_resto_search(testbot):
    testbot.push_message('!resto search burger')
    result = testbot.pop_message()
    assert result is not None

def test_resto_doc(testbot):
    testbot.push_message('!resto unvalid_command')
    result = testbot.pop_message()
    assert result == "This is not a valid command man, please use 'pick', 'search <text>' or 'yelp'"
