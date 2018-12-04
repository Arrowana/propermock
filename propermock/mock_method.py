import inspect


def _return_value_annotation_check(method, return_value):
    return_annotation = inspect.signature(method).return_annotation
    if return_annotation != inspect._empty:  # If type is annotated we are strict
        if type(return_value) != return_annotation:
            raise AssertionError('return_value was of type {} while signature is {}'.format(
                type(return_value),
                return_annotation)
            )


class _CallArgumentWithReturnValue:

    def __init__(self, method, *args, **kwargs):
        self._method = method
        self._args = args
        self._kwargs = kwargs
        self.return_value = None  # TODO: Force user to return a value

    def match(self, *args, **kwargs):
        return self._args == args and self._kwargs == kwargs

    def returns(self, return_value):
        _return_value_annotation_check(self._method, return_value)
        self.return_value = return_value


class _MockMethod:

    def __init__(self, method):
        self._method = method
        self._is_setup = False  # returns same value for all calls
        self._return_value = None
        self._called_times = 0
        self._registered_setups = []

    def __call__(self, *args, **kwargs):
        if self._is_setup:
            self._signature_check(*args, **kwargs)
            self._called_times += 1
            return self._return_value
        elif self._registered_setups:
            return self._return_from_registered_setup(*args, **kwargs)
        else:
            raise NotImplementedError('mock method is not setup')

    def _signature_check(self, *args, **kwargs):
        args = (self,) + args
        inspect.signature(self._method).bind(*args, **kwargs)

    def returns(self, return_value):
        _return_value_annotation_check(self._method, return_value)
        self._is_setup = True
        self._return_value = return_value

    def _return_from_registered_setup(self, *args, **kwargs):
        registered_setup = next(
            (registered_setup for registered_setup in self._registered_setups if registered_setup.match(*args, **kwargs)),
            None)
        if registered_setup:
            return registered_setup.return_value
        else:
            raise AssertionError('No setup for the corresponding call')

    def setup(self, *args, **kwargs) -> _CallArgumentWithReturnValue:
        self._signature_check(*args, **kwargs)
        # TODO: Prevent setup twice with same argument
        call_argument_with_return_value = _CallArgumentWithReturnValue(self._method, *args, **kwargs)
        self._registered_setups.append(call_argument_with_return_value)

        return call_argument_with_return_value

    def verify_called(self, times: int):
        assert self._called_times == times


def create_mock_method(method):
    # TODO: Fix as this is incorrect, we want a method of class_to_mock
    return _MockMethod(method)


# TODO: setup method on _MockMethod
# TODO: return_value property on _MockMethod
# TODO: add a callback
