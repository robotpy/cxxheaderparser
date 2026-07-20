import collections

import pytest

import cxxheaderparser.lexer as lexer
from cxxheaderparser.simple import parse_string


class CountingDeque(collections.deque):
    popleft_count = 0
    restore_count = 0

    def __class_getitem__(cls, item):
        return cls

    def popleft(self):
        type(self).popleft_count += 1
        return super().popleft()

    def extend(self, values):
        values = list(values)
        type(self).restore_count += len(values)
        return super().extend(values)

    def extendleft(self, values):
        values = list(values)
        type(self).restore_count += len(values)
        return super().extendleft(values)

    @classmethod
    def reset_counts(cls) -> None:
        cls.popleft_count = 0
        cls.restore_count = 0


def _count_token_buffer_touches(
    declaration_count: int, monkeypatch: pytest.MonkeyPatch
) -> int:
    monkeypatch.setattr(lexer.typing, "Deque", CountingDeque)
    CountingDeque.reset_counts()

    parse_string("int x;" * declaration_count)

    return CountingDeque.popleft_count + CountingDeque.restore_count


def test_doxygen_after_lookahead_is_not_quadratic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    small = _count_token_buffer_touches(120, monkeypatch)
    large = _count_token_buffer_touches(240, monkeypatch)

    assert large < small * 3
