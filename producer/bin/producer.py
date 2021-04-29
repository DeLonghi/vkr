import sys
# Third party import
from yaml import safe_load, YAMLError

# Local application imports
from broadcasts import ModelBroadcast

# Открываем yaml файл с конфигурацией продьюсера



# with open(sys.argv[1], newline='') as data_file:

try:
        thread = ModelBroadcast(delay=15,
                           data_file=sys.argv[1])
        thread.start()
except KeyboardInterrupt:
    pass

