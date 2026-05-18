import os
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from menu_store import load_dishes, pick_dishes


def test_load_dishes_reads_json():
    path = Path(PROJECT_ROOT) / "dishes.json"
    assert load_dishes(path) == ["黄焖鸡", "牛肉面", "麻辣烫", "盖浇饭"]


def test_pick_dishes_excludes_selected_items():
    with patch("menu_store.random.sample", return_value=["牛肉面", "麻辣烫"]):
        assert pick_dishes(["黄焖鸡", "牛肉面", "麻辣烫"], {"黄焖鸡"}) == ["牛肉面", "麻辣烫"]


def test_pick_dishes_returns_remaining_items_when_less_than_two():
    assert pick_dishes(["黄焖鸡"], set()) == ["黄焖鸡"]
