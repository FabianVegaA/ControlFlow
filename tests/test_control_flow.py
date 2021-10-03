import pytest
import logging

from source.control_flow import control_flow


def test_control_flow_decorator():
    """
    Test control flow decorator
    """

    @control_flow.catch_errors
    def _faulty_function():
        """
        Faulty function
        """
        return 1 / 0

    @control_flow.catch_errors
    def _safe_function():
        """
        Safe function
        """
        return 1

    @control_flow.safe_run
    def _test_function():
        """
        Test function
        """
        result = []

        for _ in range(10):
            result.append(_safe_function())
            result.append(_faulty_function())
        return result

    logging.info("Test function: {}".format(_test_function()))
    assert len(_test_function()) == 20
    assert set(_test_function()) == {1, None}
