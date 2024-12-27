import os
import json
from pathlib import Path

_config_path = (
    Path.home() / "AppData" / "LocalLow" / "Withered_Flower" / "AoC_Helper" / "config"
)

# create config directory if it doesn't exist
if not os.path.isdir(_config_path):
    os.makedirs(_config_path)

# create path.data file if it doesn't exist
if not os.path.isfile(_config_path / "path.data"):
    with open(_config_path / "path.data", "w") as f:
        pass

# create cookies.json file if it doesn't exist
if not os.path.isfile(_config_path / "cookies.json"):
    with open(_config_path / "cookies.json", "w") as f:
        pass

# create settings.json file if it doesn't exist
if not os.path.isfile(_config_path / "settings.json"):
    with open(_config_path / "settings.json", "w") as f:
        f.write(json.dumps({"language": "en", "last_window_pos": None}, indent=4))

cfg_path = {
    "cookies": _config_path / "cookies.json",
    "settings": _config_path / "settings.json",
    "path": _config_path / "path.data",
}

if __name__ == "__main__":
    print(_config_path)
