from unittest import mock

from wava.checker.main import loop


def test_loop_catches_keyboard_interrupt():
    check_mock = mock.MagicMock(side_effect=KeyboardInterrupt)
    cleanup_mock = mock.MagicMock()
    config = {"interval": 1}
    loop(config, check_mock, cleanup_mock)
    check_mock.assert_called_once_with(config)
    cleanup_mock.assert_called_once_with(config)
