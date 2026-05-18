import datetime
from pathlib import Path

from menu_store import load_dishes, pick_dishes
from menu_window import RecommendationWindow, show_error

try:
    from plyer import notification
except ImportError:
    class _Notification:
        @staticmethod
        def notify(**kwargs):
            return None

    notification = _Notification()


DEFAULT_DISHES_PATH = Path(__file__).resolve().with_name("dishes.json")


def is_workday():
    return datetime.datetime.now().weekday() < 5


def show_recommendation_window(dishes):
    def refresh(excluded):
        return pick_dishes(dishes, excluded)

    recommended = refresh(set())
    if not recommended:
        show_error("菜单为空", "dishes.json 里没有可推荐的菜品。")
        return False

    window = RecommendationWindow(recommended, on_refresh=refresh)
    window.show()
    return True


def main():
    if not is_workday():
        return False

    notification.notify(
        title="叮~~",
        message="该点外卖啦，记得按时吃饭~",
        timeout=8,
        app_name="点外卖提醒器",
    )

    try:
        dishes = load_dishes(DEFAULT_DISHES_PATH)
    except Exception as exc:
        show_error("菜单库读取失败", str(exc))
        return False

    return show_recommendation_window(dishes)


if __name__ == "__main__":
    main()
