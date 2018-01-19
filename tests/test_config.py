import pytest

from flotilla.config import Config


def test_file_not_found():
    with pytest.raises(IOError):
        config = Config.factory('/some/missing/file')
