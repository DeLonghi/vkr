from model import Model
import numpy as np
import pandas as pd
from itertools import cycle
# import array

conf = {"tag": "AVT10:LC475",
"rollwsize" : '72',
"history": '24',
"future": '72'}

m = Model(conf)
m._set_from_pkl('model\\resources\\restore_fuel_v5.pkl')
d = np.array([3.123, 11, 3.1231, 3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231,3.123, 11, 3.1231], dtype='f')
# d = array('f', [61.2267784, 60.56488666, 59.75663732])
# print(m.run(d, 'predict'))

ccc = pd.read_csv('C:\\vkr\producer\\resources\\fuel_test.csv')
_iterator = cycle(ccc.index)
ti = _iterator.__next__()
res = ccc.loc[ti]
res = res.dropna().to_json(orient='index')
# print(res)
send_to_consumer = {}
send_to_consumer['input'] = res
send_to_consumer['output'] = m.run(d, 'predict')
print(send_to_consumer)