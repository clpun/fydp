import numpy as np
from scipy import stats

from statsmodels.stats.multicomp import pairwise_tukeyhsd

x = np.rec.array([
(  1,   'control',  445.0469231 ),
(  2,   'control',  426.6623077 ),
(  3,   'control',  426.6623077 ),
(  4,   'control',  418.0469231 ),
(  5,   'control',  373.8161538 ),
(  6,   'control',  332.8161538 ),
(  7,   'control',  399.4315385 ),
(  8,   'control',  448.5853846 ),
(  9,   'control',  461.7392308 ),
( 10,   'control',  424.1238462 ),
( 11, 'test',  287.0469231 ),
( 12, 'test',  296.1238462 ),
( 13, 'test',  323.5853846 ),
( 14, 'test',  385.4315385 ),
( 15, 'test',  357.8161538 ),
( 16, 'test',  324.5853846 ),
( 17, 'test',  328.6623077 ),
( 18, 'test',  357.1238462 ),
( 19, 'test',  358.97 ),
( 20, 'test',  321.4315385 )], dtype=[('idx', '<i4'),
                                ('type', '|S8'),
                                ('power', 'float')])

# f_value, p_value = stats.f_oneway(x.power[0:9], x.power[10:19])
# print f_value, p_value

# result = pairwise_tukeyhsd(x['power'], x['type'])

print type(x['power'])