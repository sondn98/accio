from collections import deque
from typing import Generic, TypeVar


T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self.__stack = deque()

    def __len__(self):
        return len(self.__stack)

    def push(self, x: T):
        self.__stack.append(x)

    def pop(self) -> T:
        return self.__stack.pop()

    def peak(self) -> T:
        return self.__stack[-1]

    def empty(self) -> bool:
        return not self.__stack
