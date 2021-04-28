# Standard library imports
from yaml import safe_load, YAMLError
import sys

# Third party import

# Local application imports
from inout import StdIO

if __name__ == '__main__':
    # Инициализация моделей
    with open(sys.argv[1], 'r') as yml:
        try:
            conf = safe_load(yml)
            StdIO(conf).run()
        except YAMLError as exc:
            pass
