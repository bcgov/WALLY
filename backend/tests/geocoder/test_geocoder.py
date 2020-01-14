from api.v1.geocoder.controller import search_spaces, search_symbols
from tests.utils import get_mock_session


def test_remove_symbols():
    """ test that symbols are removed from text to prevent search errors
    """
    test_string = "a$b&|\\c<->"
    expected_string = "abc"

    subbed_string = search_symbols.sub('', test_string)
    assert subbed_string == expected_string


def test_remove_spaces():
    """ test that spaces are matched by the search_space regex
    """
    test_string = "a b        c"
    expected_string = "abc"

    subbed_string = search_spaces.sub('', test_string)
    assert subbed_string == expected_string
