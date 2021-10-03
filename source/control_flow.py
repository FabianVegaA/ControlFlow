import logging
import sys
import traceback
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Callable, List, Optional, Type


@dataclass
class ExceptionInfo:
    exc_type: Optional[Type[BaseException]]
    exc_value: Optional[BaseException]
    exc_traceback: Optional[TracebackType]

    def __str__(self):
        return (
            f"{repr(self.exc_value)}\n"
            + "=" * 60
            + "\n{}\n".format("".join(traceback.format_tb(self.exc_traceback)))
            + "=" * 60
        )


class ControlFlow:
    def __init__(self) -> None:
        self._errors: List[Exception] = []

    def _len_errors(self) -> int:
        return len(self._errors)

    def _new_error(self, error: Exception) -> None:
        self._errors.append(error)

    def _show_info(self) -> None:

        message = "\n Control Flow - "
        message += (
            f"Errors ({self._len_errors()}): \n"
            + "=" * 60
            + "".join(("\n\t{} ".format(str(e)) for e in self._errors))
        )

        logging.warn(message)

    def catch_errors(self, function: Callable) -> Callable:
        """
        This function catches errors
        - param:
            - function: function to be executed.
        - return: function result or None if error occurred.
        """

        def wrapper(*args, **kwargs) -> Any:
            result = None
            try:
                result = function(*args, **kwargs)
            except BaseException:
                self._new_error(ExceptionInfo(*sys.exc_info()))
            return result

        return wrapper

    def safe_run(self, function: Callable) -> Callable:
        """
        This function executes a function, catch errors and show the information of the errors catched.
        - param:
            - function: function to be executed.
        - return: function result or None if error occurred.
        """

        def wrapper(*args, **kwargs) -> Any:
            result = None
            try:
                result = function(*args, **kwargs)
            except BaseException:
                self._new_error(ExceptionInfo(*sys.exc_info()))

            self._show_info()
            return result

        return wrapper


control_flow: ControlFlow = ControlFlow()
