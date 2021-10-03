import traceback

class ControlFlow:
    def __init__(self):
        self._errors = []

    def _len_errors(self):
        return len(self._errors)

    def _new_error(self, error):
        self._errors.append(error)

    def _show_info(self):
        import logging

        trace = "\n\t\t".join(repr(summary) for summary in traceback.extract_stack())
        
        message = "\n- Control Flow"
        message += "\n\tErrors: " + "".join((f"\n\t\t{repr(e)} \n\t\t{trace}" for e in self._errors))

        logging.warn(message)
        
    def catch_errors(self, function):
        """
        This function catches errors
        - param:
            - function: function to be executed.
        - return: function result or None if error occurred.
        """

        def wrapper(*args, **kwargs):
            result = None
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                self._new_error(e)
            return result

        return wrapper

    def safe_run(self, function):
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                self._new_error(e)

            self._show_info()
            return result

        return wrapper


control_flow = ControlFlow()
