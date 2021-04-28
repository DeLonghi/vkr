import sys
# Third party import
from yaml import safe_load, YAMLError

# Local application imports
from broadcasts import ModelBroadcast

# Открываем yaml файл с конфигурацией продьюсера

with open(sys.argv[1], 'r') as yf:
    try:
        config = safe_load(yf)
    except YAMLError as exc:
        # TODO: Сделать лог для Producer сервисов
        pass

broadcast = config['type']
types = {'Producer': ModelBroadcast}
broadcast = types[broadcast]


id = config['id']
try:
    for th in config['threads']:
        conf = config['threads']['service_name']
        thread = broadcast(id=id,
                           delay=conf['delay']//100,
                           input=conf['input'])
        thread.start()
except KeyboardInterrupt:
    pass

