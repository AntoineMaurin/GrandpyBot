import pytest

from clean_data import CleanData

class TestCleanData:

    def test_clean_data(self):
        initial_data = "<p>\n</p>\n<p>La <b>cité    Paradis</b> est..."

        test_result = CleanData.clean(initial_data)

        assert test_result == "La cité Paradis est..."

    def test_clean_data_raises_error(self):
        initial_data = "<p>\n</p>\n<p>La <b>cité    Paradis</b> est..."

        test_result = CleanData.clean(initial_data)

        with pytest.raises(AssertionError):
            assert test_result != "La cité Paradis est..."
