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

def test_yelp_pick(testbot):
    testbot.push_message('!yelp pick')
    result = testbot.pop_message()
    assert result is not None

def test_yelp_search(testbot):
    testbot.push_message('!yelp search burger')
    result = testbot.pop_message()
    assert result is not None
