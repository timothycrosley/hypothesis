# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2017 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

from random import Random

import hypothesis.strategies as st
from hypothesis import find, given, example
from hypothesis.control import _current_build_context
from tests.common.utils import checks_deprecated_behaviour


@given(st.integers())
def test_deterministic_examples_are_deterministic(seed):
    with _current_build_context.with_value(None):
        assert st.lists(st.integers()).example(Random(seed)) == \
            st.lists(st.integers()).example(Random(seed))


def test_does_not_always_give_the_same_example():
    s = st.integers()
    assert len(set(
        s.example() for _ in range(100)
    )) >= 10


@checks_deprecated_behaviour
@example(False)
@given(st.booleans())
def test_example_inside_given(b):
    st.integers().example()


@checks_deprecated_behaviour
def test_example_inside_find():
    find(st.integers(0, 100), lambda x: st.integers().example())


@checks_deprecated_behaviour
def test_example_inside_strategy():
    st.booleans().map(lambda x: st.integers().example()).example()
