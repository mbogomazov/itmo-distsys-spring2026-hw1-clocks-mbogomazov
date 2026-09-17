import heapq
from typing import Dict

VectorClock = Dict[str, int]


def happens_before(a: VectorClock, b: VectorClock) -> bool:
    """a -> b  <=>  для всех процессов a[k] <= b[k] и хотя бы для одного a[k] < b[k]."""
    # Отсутствующий в словаре процесс считаем нулем
    processes: set[str] = set(a.keys()) | set(b.keys())
    all_less_or_equal: bool = all(a.get(p, 0) <= b.get(p, 0) for p in processes)
    some_strictly_less: bool = any(a.get(p, 0) < b.get(p, 0) for p in processes)
    return all_less_or_equal and some_strictly_less


def partial_sort(timestamps: list[VectorClock]) -> list[VectorClock]:
    """Топологическая сортировка (алгоритм Кана) графа отношения happens-before."""
    m: int = len(timestamps)

    # Граф: ребро i -> j, если событие i happens-before события j
    successors: list[list[int]] = [[] for _ in range(m)]
    in_degree: list[int] = [0] * m
    for i in range(m):
        for j in range(m):
            if i != j and happens_before(timestamps[i], timestamps[j]):
                successors[i].append(j)
                in_degree[j] += 1

    # "Готовые" события: все их предшественники уже в ответе.
    # Куча по индексу делает результат детерминированным: из готовых берем самое раннее во входе.
    ready: list[int] = [i for i in range(m) if in_degree[i] == 0]
    heapq.heapify(ready)

    result: list[VectorClock] = []
    while ready:
        i: int = heapq.heappop(ready)
        result.append(timestamps[i])
        for j in successors[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                heapq.heappush(ready, j)

    return result
