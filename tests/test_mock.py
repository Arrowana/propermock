import pytest
from propermock.mock import Mock


def test_mock_has_mocked_class_methods():
    farm_mock = Mock(_Farm)

    assert callable(farm_mock.harvest_potato)
    assert callable(farm_mock.harvest_vegetables)

    # TODO: use stronger assertion below when Mock allows it
    # assert inspect.ismethod(farm_mock.harvest_potato)
    # assert inspect.ismethod(farm_mock.harvest_all_vegetables)


def test_mock_method_raise_exception_when_not_setup():
    farm_mock = Mock(_Farm)

    with pytest.raises(NotImplementedError):
        farm_mock.harvest_potato()


def test_mock_method_return_value_passed_to_returns():
    farm_mock = Mock(_Farm)

    farm_mock.harvest_potato.returns(10)

    assert farm_mock.harvest_potato() == 10


def test_raise_exception_when_method_called_with_wrong_signature():
    farm_mock = Mock(_Farm)

    farm_mock.harvest_potato.returns(1)
    farm_mock.harvest_vegetables.returns(None)

    with pytest.raises(TypeError):
        farm_mock.harvest_potato(1)

    with pytest.raises(TypeError):
        farm_mock.harvest_vegetables()


def test_mock_method_verify_called_does_not_raise_when_called_with_right_times():
    farm_mock = Mock(_Farm)
    farm_mock.harvest_potato.returns(1)

    farm_mock.harvest_potato()

    farm_mock.harvest_potato.verify_called(1)


def test_mock_method_verify_called_raises_when_called_with_wrong_number_of_times():
    farm_mock = Mock(_Farm)
    farm_mock.harvest_potato.returns(1)

    farm_mock.harvest_potato()

    with pytest.raises(AssertionError):
        farm_mock.harvest_potato.verify_called(0)


# TODO: def test_raise_exception_when_method_called_with_argument_with_type_not_matching_return_annotation():
#     farm_mock = Mock(_MegaFarm)
#
#     farm_mock.harvest_potato.returns(1)
#
#     with pytest.raises(TypeError):
#         farm_mock.harvest_potato(1.02)

def test_mock_method_setup_call_returns_value_when_called_with_matching_params():
    farm_mock = Mock(_Farm)
    farm_mock.harvest_vegetables.setup(['potato', 'eggplant']).returns(1)

    assert farm_mock.harvest_vegetables(['potato', 'eggplant']) == 1


def test_mock_method_setup_call_returns_corresponding_value_when_called_with_certain_params():
    farm_mock = Mock(_Farm)
    farm_mock.harvest_vegetables.setup(['potato', 'eggplant']).returns(2)
    farm_mock.harvest_vegetables.setup(['onion'], in_basket=False).returns(3)

    assert farm_mock.harvest_vegetables(['potato', 'eggplant']) == 2
    assert farm_mock.harvest_vegetables(['onion'], in_basket=False) == 3


def test_mock_method_setup_call_raises_when_called_with_non_matching_params():
    farm_mock = Mock(_Farm)
    farm_mock.harvest_vegetables.setup(['potato', 'eggplant']).returns(1)

    with pytest.raises(AssertionError, message='No setup for the corresponding call'):
        farm_mock.harvest_vegetables(['eggplant', 'potato'])

    with pytest.raises(AssertionError, message='No setup for the corresponding call'):
        farm_mock.harvest_vegetables([])

    with pytest.raises(AssertionError, message='No setup for the corresponding call'):
        farm_mock.harvest_vegetables([1, 2])

    with pytest.raises(AssertionError, message='No setup for the corresponding call'):
        farm_mock.harvest_vegetables(112)


class _Farm:

    def harvest_potato(self):
        pass

    def harvest_vegetables(self, vegetables_to_harvest: list, in_basket=True):
        pass
