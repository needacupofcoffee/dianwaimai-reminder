import os
import sys
from unittest.mock import MagicMock, patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from menu_window import RecommendationWindow


@patch("menu_window.tk.Frame")
@patch("menu_window.tk.Button")
@patch("menu_window.tk.Label")
@patch("menu_window.tk.Tk")
@patch("menu_window.random.choice", return_value="文案 A")
def test_window_sets_topmost_and_does_not_schedule_auto_close(
    mock_choice, mock_tk, mock_label, mock_button, mock_frame
):
    fake_root = MagicMock()
    fake_frame = MagicMock()
    mock_tk.return_value = fake_root
    mock_frame.return_value = fake_frame

    RecommendationWindow(["黄焖鸡", "牛肉面"], on_refresh=lambda excluded: None)

    fake_root.attributes.assert_any_call("-topmost", True)
    fake_root.after.assert_not_called()
    fake_root.configure.assert_called_once()
    assert mock_label.call_count >= 4
    assert mock_button.call_count == 2
    assert mock_frame.call_count >= 4


@patch("menu_window.tk.Frame")
@patch("menu_window.tk.Button")
@patch("menu_window.tk.Label")
@patch("menu_window.tk.Tk")
@patch("menu_window.random.choice", side_effect=["初始文案", "刷新文案"])
def test_refresh_passes_current_exclusions_to_callback(mock_choice, mock_tk, mock_label, mock_button, mock_frame):
    fake_root = MagicMock()
    callback = MagicMock(return_value=["麻辣烫", "盖浇饭"])
    label_mocks = []

    mock_tk.return_value = fake_root
    mock_frame.side_effect = lambda *args, **kwargs: MagicMock()

    def build_label(*args, **kwargs):
        label = MagicMock()
        label_mocks.append(label)
        return label

    mock_label.side_effect = build_label

    window = RecommendationWindow(["黄焖鸡", "牛肉面"], on_refresh=callback)
    window.excluded = {"馄饨"}
    previous_rows = list(window.dish_rows)
    window.handle_refresh()

    callback.assert_called_once_with({"黄焖鸡", "牛肉面", "馄饨"})
    assert window.dishes == ["麻辣烫", "盖浇饭"]
    assert window.description_message == "刷新文案"
    assert len(window.dish_rows) == 2
    label_mocks[2].config.assert_called_once_with(text="刷新文案")
    for row in previous_rows:
        row.destroy.assert_called_once()
