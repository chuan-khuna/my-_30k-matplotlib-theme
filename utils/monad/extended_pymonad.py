# Python 3.10, 3.11
# PyMonad==2.4.0

from pymonad.either import Left, Right, Either as pyEither

from typing import Any, Callable, Generic, TypeVar


M = TypeVar('M')
S = TypeVar('S')
T = TypeVar('T')


class Either(pyEither, Generic[M, T]):
    """Extend pymonad Either"""

    def __rshift__(self, func):
        """Use `>>` as a shorthand for `bind`"""
        return self.bind(func)

    def __or__(self, func):
        """Use `|` as a shorthand for `bind`"""
        return self.bind(func)

    def get_error(self) -> str | None:
        if self.is_left():
            return self.monoid[0]

        return None


def Left(value: M) -> Either[M, Any]:
    """Creates a value of the first possible type in the Either monad."""
    return Either(None, (value, False))


def Right(value: T) -> Either[Any, T]:
    """Creates a value of the second possible type in the Either monad."""
    return Either(value, (None, True))
