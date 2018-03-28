"""Basic output validation tests"""

import food

# pytest
extra_plugin_dir = '.'
pytest_plugins = ['errbot.backends.test']


def test_restopicker(testbot):
    testbot.push_message('!restopicker')
    result = testbot.pop_message()
    assert result is not None
