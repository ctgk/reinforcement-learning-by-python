import pytest

import rlpy


def test_rlpy():
    assert rlpy.__version__ == '0.0.1'


if __name__ == "__main__":
    pytest.main([__file__])
