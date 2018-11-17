import inspect


class _MockMethod:

    def __init__(self, method):
        self._method = method
        self._is_setup = False
        self._return_value = None
        self._called_times = 0

    def __call__(self, *args, **kwargs):
        if self._is_setup:
            # signature check
            args = (self,) + args
            inspect.signature(self._method).bind(*args, **kwargs)
            self._called_times += 1
            return self._return_value
        else:
            raise NotImplementedError('mock method is not setup')

    def returns(self, return_value):
        return_annotation = inspect.signature(self._method).return_annotation
        if return_annotation != inspect._empty:  # If type is annotated we are strict
            if type(return_value) != return_annotation:
                raise AssertionError('return_value was of type {} while signature is {}'.format(
                    type(return_value),
                    return_annotation)
                )

        self._is_setup = True
        self._return_value = return_value

    def verify_called(self, times: int):
        assert self._called_times == times


def create_mock_method(method):
    # TODO: Fix as this is incorrect, we want a method of class_to_mock
    return _MockMethod(method)


# TODO: setup method on _MockMethod
# TODO: return_value property on _MockMethod
# TODO: add a callback
