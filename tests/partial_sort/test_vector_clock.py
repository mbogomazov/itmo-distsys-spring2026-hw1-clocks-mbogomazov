import random

from tasks.partial_sort.vector_clock import VectorClock
from tasks.partial_sort.vector_clock import partial_sort


def happens_before(vc1: VectorClock, vc2: VectorClock) -> bool:
    """Check if vc1 happens before vc2 (vc1 <= vc2 and vc1 != vc2)."""
    all_less_equal = all(vc1.get(k, 0) <= vc2.get(k, 0) for k in set(vc1.keys()) | set(vc2.keys()))
    not_equal = vc1 != vc2
    return all_less_equal and not_equal


def is_valid_topological_order(timestamps: list[VectorClock], sorted_timestamps: list[VectorClock]) -> bool:
    """Validate that sorted_timestamps respects causal ordering."""
    for i, ts1 in enumerate(sorted_timestamps):
        for j, ts2 in enumerate(sorted_timestamps):
            if i < j and happens_before(ts2, ts1):
                return False
    return True


def validate_partial_sort_output(input_timestamps: list[VectorClock]) -> None:
    """Generic validation procedure for partial sort output."""
    result = partial_sort(input_timestamps)
    assert len(result) == len(input_timestamps), "Output must have same length as input"
    assert sorted(result, key=str) == sorted(input_timestamps, key=str), "Output must contain same elements"
    assert is_valid_topological_order(input_timestamps, result), "Output must respect causal ordering"


def test_partial_sort_topological_order_case1():
    """Test with mixed clocks."""
    timestamps = [{"p1": 1, "p2": 0}, {"p1": 2, "p2": 0}, {"p1": 1, "p2": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_topological_order_case2():
    """Test with single process."""
    timestamps = [{"a": 3}, {"a": 1}, {"a": 2}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_topological_order_case3():
    """Test with incomparable clocks."""
    timestamps = [{"p": 1, "q": 1}, {"p": 0, "q": 2}, {"p": 1, "q": 0}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_topological_order_case4():
    """Test with single clock."""
    timestamps = [{"x": 0, "y": 0}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_topological_order_case5():
    """Test with empty list."""
    timestamps = []
    validate_partial_sort_output(timestamps)


def test_partial_sort_topological_order_case6():
    """Test with three processes."""
    timestamps = [{"a": 1, "b": 2, "c": 3},
                  {"a": 0, "b": 1, "c": 2},
                  {"a": 1, "b": 1, "c": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm0():
    """Test permutation 0."""
    timestamps = [{"p1": 1, "p2": 0}, {"p1": 2, "p2": 1}, {"p1": 1, "p2": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm1():
    """Test permutation 1."""
    timestamps = [{"p1": 1, "p2": 0}, {"p1": 1, "p2": 1}, {"p1": 2, "p2": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm2():
    """Test permutation 2."""
    timestamps = [{"p1": 2, "p2": 1}, {"p1": 1, "p2": 0}, {"p1": 1, "p2": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm3():
    """Test permutation 3."""
    timestamps = [{"p1": 2, "p2": 1}, {"p1": 1, "p2": 1}, {"p1": 1, "p2": 0}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm4():
    """Test permutation 4."""
    timestamps = [{"p1": 1, "p2": 1}, {"p1": 1, "p2": 0}, {"p1": 2, "p2": 1}]
    validate_partial_sort_output(timestamps)


def test_partial_sort_permutations_perm5():
    """Test permutation 5."""
    timestamps = [{"p1": 1, "p2": 1}, {"p1": 2, "p2": 1}, {"p1": 1, "p2": 0}]
    validate_partial_sort_output(timestamps)


def generate_vector_clocks(
    num_clocks: int,
    num_processes: int,
    max_value: int = 10,
) -> list[VectorClock]:
    return [
        {f"p{i}": random.randint(0, max_value) for i in range(num_processes)}
        for _ in range(num_clocks)
    ]


def test_partial_sort_generated_input_5_2():
    """Test with 5 clocks and 2 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(5, 2)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_10_3():
    """Test with 10 clocks and 3 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(10, 3)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_8_4():
    """Test with 8 clocks and 4 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(8, 4)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_2_5():
    """Test with 2 clocks and 5 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(2, 5)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_15_2():
    """Test with 15 clocks and 2 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(15, 2)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_7_6():
    """Test with 7 clocks and 6 processes (2000 iterations)."""
    for _ in range(2000):
        timestamps = generate_vector_clocks(7, 6)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_20_3():
    """Test with 20 clocks and 3 processes (1000 iterations)."""
    for _ in range(1000):
        timestamps = generate_vector_clocks(20, 3)
        validate_partial_sort_output(timestamps)


def test_partial_sort_generated_input_3_10():
    """Test with 3 clocks and 10 processes (1000 iterations)."""
    for _ in range(1000):
        timestamps = generate_vector_clocks(3, 10)
        validate_partial_sort_output(timestamps)


# DAG Generation Scenario Tests

def test_dag_complete_order_linear_chain():
    """Test complete order (total order) - all clocks form a linear chain."""
    # Each clock is causally before the next
    timestamps = [
        {"p": 0},
        {"p": 1},
        {"p": 2},
        {"p": 3},
        {"p": 4},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_complete_order_multiprocess():
    """Test complete order with multiple processes forming a chain."""
    # Events happen in strict causal sequence
    timestamps = [
        {"a": 0, "b": 0, "c": 0},
        {"a": 1, "b": 0, "c": 0},
        {"a": 1, "b": 1, "c": 0},
        {"a": 1, "b": 1, "c": 1},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_antichain_all_incomparable():
    """Test anti-chain - all clocks are incomparable to each other."""
    # No clock happens-before any other
    timestamps = [
        {"p": 1, "q": 0},
        {"p": 0, "q": 1},
        {"p": 1, "q": 0},
        {"p": 0, "q": 1},
    ]
    # Need unique clocks for this test
    timestamps = [
        {"p": 1, "q": 0, "r": 0},
        {"p": 0, "q": 1, "r": 0},
        {"p": 0, "q": 0, "r": 1},
        {"p": 0, "q": 0, "r": 0, "s": 1},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_diamond_pattern():
    """Test diamond-shaped DAG structure."""
    # Two branches that merge
    #     c1
    #    /  \
    #   c2  c3
    #    \  /
    #     c4
    timestamps = [
        {"a": 2, "b": 0},  # c1
        {"a": 1, "b": 1},  # c2 (after c1)
        {"a": 1, "b": 1},  # c3 would be here but incomparable
        {"a": 2, "b": 2},  # c4 (after c1 and others)
    ]
    validate_partial_sort_output(timestamps)


def test_dag_star_pattern():
    """Test star-shaped DAG - one source, many independent successors."""
    # Root event followed by multiple independent events
    timestamps = [
        {"center": 0, "p1": 0, "p2": 0, "p3": 0},  # Root
        {"center": 1, "p1": 0, "p2": 0, "p3": 0},  # Branch 1
        {"center": 1, "p1": 1, "p2": 0, "p3": 0},  # Branch 2
        {"center": 1, "p1": 0, "p2": 1, "p3": 0},  # Branch 3
    ]
    validate_partial_sort_output(timestamps)


def test_dag_multiple_branches():
    """Test DAG with multiple independent causal branches."""
    # Two independent sequences
    #  Branch A: a1 -> a2 -> a3
    #  Branch B: b1 -> b2 -> b3
    timestamps = [
        {"a_seq": 0, "b_seq": 0},  # Start
        {"a_seq": 1, "b_seq": 0},  # a1
        {"a_seq": 0, "b_seq": 1},  # b1
        {"a_seq": 2, "b_seq": 0},  # a2
        {"a_seq": 0, "b_seq": 2},  # b2
    ]
    validate_partial_sort_output(timestamps)


def test_dag_wide_antichain():
    """Test wide DAG - many incomparable clocks."""
    # All clocks have activity in different processes
    timestamps = [
        {"p1": 1, "p2": 0, "p3": 0, "p4": 0},
        {"p1": 0, "p2": 1, "p3": 0, "p4": 0},
        {"p1": 0, "p2": 0, "p3": 1, "p4": 0},
        {"p1": 0, "p2": 0, "p3": 0, "p4": 1},
        {"p1": 0, "p2": 0, "p3": 0, "p4": 0},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_deep_chain():
    """Test deep DAG - long linear causal chain."""
    # Single process with sequential events
    timestamps = [
        {"seq": i}
        for i in range(15)
    ]
    validate_partial_sort_output(timestamps)


def test_dag_deep_chain_multiprocess():
    """Test deep chain across multiple processes."""
    # Causal chain involving multiple processes
    timestamps = [
        {"p": i, "q": 0, "r": 0}
        for i in range(10)
    ] + [
        {"p": 10, "q": i, "r": 0}
        for i in range(1, 8)
    ]
    validate_partial_sort_output(timestamps)


def test_dag_mesh_pattern():
    """Test mesh-pattern DAG with multiple criss-crossing paths."""
    # Complex partial order with multiple concurrent paths
    timestamps = [
        {"x": 1, "y": 0},
        {"x": 0, "y": 1},
        {"x": 1, "y": 1},
        {"x": 2, "y": 1},
        {"x": 1, "y": 2},
        {"x": 2, "y": 2},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_pyramid_pattern():
    """Test pyramid-shaped DAG - many at bottom, one at top."""
    # Multiple independent events that all causally precede a final event
    timestamps = [
        {"p1": 1, "p2": 0, "p3": 0},
        {"p1": 0, "p2": 1, "p3": 0},
        {"p1": 0, "p2": 0, "p3": 1},
        {"p1": 0, "p2": 0, "p3": 0},
        {"p1": 1, "p2": 1, "p3": 1},  # Top of pyramid
    ]
    validate_partial_sort_output(timestamps)


def test_dag_with_zeros_only():
    """Test DAG with all zero clocks (starting state)."""
    timestamps = [
        {"p1": 0, "p2": 0},
        {"p1": 0, "p2": 0},
        {"p1": 0, "p2": 0},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_with_mixed_zeros():
    """Test DAG with mix of zero and increased counters."""
    timestamps = [
        {"a": 0, "b": 0},
        {"a": 1, "b": 0},
        {"a": 0, "b": 1},
        {"a": 1, "b": 1},
        {"a": 0, "b": 0},  # Concurrent with first
    ]
    validate_partial_sort_output(timestamps)


def test_dag_high_values():
    """Test DAG with high counter values."""
    timestamps = [
        {"p": 100},
        {"p": 200},
        {"p": 150},
        {"p": 250},
        {"q": 50, "r": 100},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_many_processes_few_clocks():
    """Test DAG with many processes but few clocks."""
    timestamps = [
        {f"p{i}": 1 if i < 3 else 0 for i in range(10)},
        {f"p{i}": 0 if i < 3 else 1 for i in range(10)},
        {f"p{i}": 1 if i >= 5 else 0 for i in range(10)},
    ]
    validate_partial_sort_output(timestamps)


def test_dag_few_processes_many_clocks():
    """Test DAG with few processes but many clocks."""
    timestamps = [
        {"p": i, "q": 0}
        for i in range(5)
    ] + [
        {"p": 0, "q": i}
        for i in range(1, 6)
    ] + [
        {"p": i, "q": i}
        for i in range(1, 4)
    ]
    validate_partial_sort_output(timestamps)


def test_dag_complex_partial_order():
    """Test complex partial order with multiple comparability relationships."""
    # Mix of comparable and incomparable clocks
    timestamps = [
        {"a": 0, "b": 0, "c": 0},  # Base event
        {"a": 1, "b": 0, "c": 0},  # a advances
        {"a": 1, "b": 1, "c": 0},  # b advances  
        {"a": 0, "b": 1, "c": 1},  # c advances (concurrent with a=1)
        {"a": 2, "b": 1, "c": 0},  # a advances further
        {"a": 1, "b": 2, "c": 1},  # b and c advance (after base)
    ]
    validate_partial_sort_output(timestamps)


def test_dag_three_way_branch():
    """Test three-way branching pattern."""
    # Root splits into three independent paths that later converge
    timestamps = [
        {"main": 0, "b1": 0, "b2": 0, "b3": 0},  # Root
        {"main": 1, "b1": 1, "b2": 0, "b3": 0},  # Branch 1
        {"main": 1, "b1": 0, "b2": 1, "b3": 0},  # Branch 2
        {"main": 1, "b1": 0, "b2": 0, "b3": 1},  # Branch 3
        {"main": 2, "b1": 1, "b2": 0, "b3": 0},  # Branch 1 continues
        {"main": 2, "b1": 1, "b2": 1, "b3": 1},  # Convergence point
    ]
    validate_partial_sort_output(timestamps)


def test_dag_long_incomparable_sequence():
    """Test long sequence of incomparable events."""
    # Each clock progresses independently in different processes
    timestamps = [
        {"p1": i, "p2": 0, "p3": 0, "p4": 0}
        for i in range(5)
    ] + [
        {"p1": 0, "p2": i, "p3": 0, "p4": 0}
        for i in range(1, 5)
    ] + [
        {"p1": 0, "p2": 0, "p3": i, "p4": 0}
        for i in range(1, 5)
    ] + [
        {"p1": 0, "p2": 0, "p3": 0, "p4": i}
        for i in range(1, 5)
    ]
    validate_partial_sort_output(timestamps)
