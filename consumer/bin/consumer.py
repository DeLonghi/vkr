from receivers import Receiver

models = {}
# with open('config.yml', 'r') as yf:
#     config = safe_load(yf)
#     for model in config['models'].values():
#         models[model['id']] = model['threads']

Receiver(models).run()

