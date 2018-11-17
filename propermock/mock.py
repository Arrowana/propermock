import inspect
from .mock_method import create_mock_method


class Mock:

    def __init__(self, class_to_mock):
        self._class_to_mock = class_to_mock

        member_tuples = inspect.getmembers(class_to_mock)
        non_builtin_member_tuples = member_tuples
        for name, type in non_builtin_member_tuples:
            # TODO: Better builtins exclusion
            # TODO: add privates mocking so we can complain if called on mock
            member = getattr(class_to_mock, name)
            # TODO: Can we do better than isfunction, ismethod on class is not possible...
            if inspect.isfunction(member) and not name.startswith('__'):
                # print('Mockable method {}, {}'.format(name, type))
                setattr(self, name, create_mock_method(member))
