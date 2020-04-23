from copy import deepcopy

from piet.context import Context


def test_same_context():
    c1 = Context(stack=[1, 2, 3], value=4)
    c2 = Context(stack=[1, 2, 3], value=4)
    assert c1 == c2


def test_distinct_stack():
    c1 = Context(stack=[1, 2, 3], value=4)
    c2 = Context(stack=[1, 3], value=4)
    assert c1 != c2


def test_distinct_value():
    c1 = Context(stack=[1, 2, 3], value=4)
    c2 = Context(stack=[1, 2, 3], value=5)
    assert c1 != c2


def test_repr():
    c = Context(stack=[1, 2, 3], value=4)
    assert repr(c) == 'Context(stack = [1, 2, 3], value = 4)'


def test_repr_no_stack():
    c = Context(value=4)
    assert repr(c) == 'Context(stack = [], value = 4)'


def test_repr_no_value():
    c = Context(stack=[1, 2, 3])
    assert repr(c) == 'Context(stack = [1, 2, 3])'


def test_str():
    c = Context(stack=[1, 2, 3], value=4)
    assert str(c) == '[1, 2, 3]  4'


def test_str_no_stack():
    c = Context(value=4)
    assert str(c) == '[]  4'


def test_str_no_value():
    c = Context(stack=[1, 2, 3])
    assert str(c) == '[1, 2, 3]'


def test_deepcopy():
    c1 = Context(stack=[1, 2, 3], value=4)
    c2 = deepcopy(c1)

    assert c1 == c2
    assert c1.stack is not c2.stack
