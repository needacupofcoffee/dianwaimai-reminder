import json
import random


def load_dishes(path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["dishes"]


def pick_dishes(dishes, excluded=None, count=2):
    excluded = set(excluded or [])
    candidates = [dish for dish in dishes if dish not in excluded]
    if not candidates:
        return []
    if len(candidates) <= count:
        return candidates
    return random.sample(candidates, count)
