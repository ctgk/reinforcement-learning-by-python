import pytest

from rlpy import State


@pytest.fixture(params=[
    {
        'state': State(),
        'row': -1,
        'col': -1,
        'repr': '<State: [r=-1, c=-1]>',
        'clone': State(),
        'hash': hash((-1, -1)),
    },
    {
        'state': State(2, 3),
        'row': 2,
        'col': 3,
        'repr': '<State: [r=2, c=3]>',
        'clone': State(2, 3),
        'hash': hash((2, 3)),
    },
])
def parameter(request):
    return request.param


def test_row(parameter):
    state = parameter['state']
    actual = state.row
    expected = parameter['row']
    assert actual == expected


def test_col(parameter):
    state = parameter['state']
    actual = state.col
    expected = parameter['col']
    assert actual == expected


def test_repr(parameter):
    state = parameter['state']
    actual = repr(state)
    expected = parameter['repr']
    assert actual == expected


def test_clone(parameter):
    state = parameter['state']
    actual = state.clone()
    expected = parameter['clone']
    assert hash(actual) == hash(expected)


def test_hash(parameter):
    state = parameter['state']
    actual = hash(state)
    expected = parameter['hash']
    assert actual == expected


if __name__ == '__main__':
    pytest.main([__file__])
