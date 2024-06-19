from typing import Any, List


def coalesce_idx(lst: List[Any]):
    if not lst:
        return -1

    for i in range(len(lst)):
        if lst[i] is None:
            return i

    return -1
