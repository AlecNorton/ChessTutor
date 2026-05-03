import pytest
from calculate_mood.calculate_mood_aggregator import calculate_mood_from_nodes


def test_single_node():
    assert calculate_mood_from_nodes({'dummy_node': 1.0}, {'dummy_node':1.0}) == pytest.approx(1.0)


def test_weighting():
    vals = {'a': 1.0, 'b': 0.5}
    w = {'a': 2.0, 'b': 1.0}
    assert calculate_mood_from_nodes(vals, w) == pytest.approx((2*1.0 + 1*0.5)/(2+1))


def test_missing_node():
    assert calculate_mood_from_nodes({}, {}) == pytest.approx(0.0)


def test_zero_weights():
    assert calculate_mood_from_nodes({'x':1.0}, {'x':0.0}) == pytest.approx(0.0)


if __name__ == '__main__':
    # Simple test runner that doesn't require pytest
    from calculate_mood.calculate_mood_aggregator import calculate_mood_from_nodes as run_calc

    def approx(a, b, eps=1e-6):
        if abs(a - b) < eps:
            return True
        raise AssertionError(f"{a} != {b}")

    # Run tests
    approx(run_calc({'dummy_node': 1.0}, {'dummy_node':1.0}), 1.0)
    vals = {'a': 1.0, 'b': 0.5}
    w = {'a': 2.0, 'b': 1.0}
    expected = (2*1.0 + 1*0.5)/(2+1)
    approx(run_calc(vals, w), expected)
    approx(run_calc({}, {}), 0.0)
    approx(run_calc({'x':1.0}, {'x':0.0}), 0.0)
    print('ALL TESTS PASSED')

