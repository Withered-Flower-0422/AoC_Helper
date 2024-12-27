import csv
from pprint import pprint

from source import src_path

with open(src_path["language"], "r", encoding="utf-8") as f:
    _reader = csv.reader(f)
    _langs = next(_reader)

    language = {
        rows[0].replace(r"\n", "\n"): {
            _langs[i]: rows[i].replace(r"\n", "\n") for i in range(1, len(rows))
        }
        for rows in _reader
    }

if __name__ == "__main__":
    pprint(language)
