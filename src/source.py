import os
import sys
from pprint import pprint

_base_path = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir


def _get_path(*args):
    return os.path.join(_base_path, *args)


src_path = {
    # icon
    "icon": _get_path("icon", "aoc_icon.ico"),
    # lang
    "language": _get_path("language", "language.csv"),
}


if __name__ == "__main__":
    pprint({path: src_path[path] for path in src_path})
