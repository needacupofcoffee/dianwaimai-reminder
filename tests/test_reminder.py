import datetime
import os
import sys
from unittest.mock import MagicMock, patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import reminder


def test_monday_is_workday():
    fake_datetime = datetime.datetime(2024, 5, 6)
    mock_dt = MagicMock()
    mock_dt.now.return_value = fake_datetime
    with patch.object(reminder.datetime, "datetime", mock_dt):
        assert reminder.is_workday()


def test_sunday_is_not_workday():
    fake_datetime = datetime.datetime(2024, 5, 12)
    mock_dt = MagicMock()
    mock_dt.now.return_value = fake_datetime
    with patch.object(reminder.datetime, "datetime", mock_dt):
        assert not reminder.is_workday()


def test_show_recommendation_window_uses_session_exclusions():
    dishes = ["黄焖鸡", "牛肉面", "麻辣烫", "盖浇饭"]

    with patch("reminder.pick_dishes", side_effect=[["黄焖鸡", "牛肉面"], ["麻辣烫", "盖浇饭"]]) as mock_pick, patch(
        "reminder.RecommendationWindow"
    ) as mock_window:
        window = MagicMock()
        mock_window.return_value = window

        assert reminder.show_recommendation_window(dishes) is True
        refresh_callback = mock_window.call_args.kwargs["on_refresh"]
        assert refresh_callback({"黄焖鸡", "牛肉面"}) == ["麻辣烫", "盖浇饭"]

    mock_pick.assert_any_call(dishes, set())
    assert mock_window.call_args.args[0] == ["黄焖鸡", "牛肉面"]
    mock_pick.assert_any_call(dishes, {"黄焖鸡", "牛肉面"})
    window.show.assert_called_once()


def test_show_recommendation_window_reports_empty_menu():
    with patch("reminder.pick_dishes", return_value=[]), patch("reminder.show_error") as mock_error:
        assert reminder.show_recommendation_window([]) is False

    mock_error.assert_called_once_with("菜单为空", "dishes.json 里没有可推荐的菜品。")


def test_main_sends_notification_and_opens_window_on_workday():
    mock_notification = MagicMock()
    with patch("reminder.notification", mock_notification), patch("reminder.load_dishes", return_value=["黄焖鸡", "牛肉面"]), patch(
        "reminder.show_recommendation_window", return_value=True
    ) as mock_window, patch("reminder.is_workday", return_value=True):
        assert reminder.main() is True

    mock_notification.notify.assert_called_once()
    mock_window.assert_called_once_with(["黄焖鸡", "牛肉面"])


def test_main_does_nothing_on_weekend():
    mock_notification = MagicMock()
    with patch("reminder.notification", mock_notification), patch("reminder.load_dishes") as mock_load, patch(
        "reminder.show_recommendation_window"
    ) as mock_window, patch("reminder.is_workday", return_value=False):
        assert reminder.main() is False

    mock_notification.notify.assert_not_called()
    mock_load.assert_not_called()
    mock_window.assert_not_called()


def test_main_returns_false_when_menu_load_fails():
    mock_notification = MagicMock()
    with patch("reminder.notification", mock_notification), patch("reminder.load_dishes", side_effect=OSError("boom")), patch(
        "reminder.show_error"
    ) as mock_error, patch("reminder.show_recommendation_window") as mock_window, patch(
        "reminder.is_workday", return_value=True
    ):
        assert reminder.main() is False

    mock_notification.notify.assert_called_once()
    mock_error.assert_called_once_with("菜单库读取失败", "boom")
    mock_window.assert_not_called()
