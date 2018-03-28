"""Basic output validation tests"""

import food

# pytest
extra_plugin_dir = '.'
pytest_plugins = ['errbot.backends.test']


def test_resto_pick(testbot):
    testbot.push_message('!resto pick')
    result = testbot.pop_message()
    assert result is not None

def test_resto_yelp(testbot):
    testbot.push_message('!resto yelp')
    result = testbot.pop_message()
    assert result is not None

def test_resto_doc(testbot):
    testbot.push_message('!resto unvalid_command')
    result = testbot.pop_message()
    assert result == "This is not a valid command man, please use 'pick' or 'yelp'"
