# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 21:14:27 2019
@author: Chengyi.zhang
"""

from docplex.mp.model import Model

import numpy as np

#集合设置
I = 15
J = 5
M = 2
T = 10

#参数设置
c = 400
f = 1000
a = 0.1
b = 0.1

d = \
[[41.23,	41.23,	56.57,	35.00,	0.00 ],
 [60.21,	47.17,	40.31,	0.00,	35.00],
 [50.00,	30.00,	0.00,	40.31,	56.57],
 [20.00,	40.00,	70.00,	76.32,	50.00],
 [44.72,	28.28,	22.36,	20.62,	36.06],
 [20.62,	36.67,	65.00,	80.62,	60.54],
 [14.14,	31.62,	60.83,	62.65,	36.06],
 [60.21,	61.85,	75.00,	44.72,	20.62],
 [53.85,	36.06,	20.00,	60.21,	72.11],
 [20.00,	0.00,	30.00,	47.17,	41.23],
 [58.31,	50.99,	53.85,	18.03,	22.36],
 [53.24,	58.60,	76.38,	51.66,	19.85],
 [ 0.00,	20.00,	50.00,	60.21,	41.23],
 [34.21,	15.81,	19.24,	50.45,	54.13],
 [58.31,	42.43,	30.00,	11.18,	41.23]]
d = np.array(d)

w = \
[[33,	23,	47,	35,	51,	44,	29,	55,	26,	20],
 [30,	55,	37,	25,	57,	29,	21,	25,	41,	51],
 [56,	29,	27,	42,	60,	25,	35,	27,	26,	50],
 [51,	60,	40,	54,	37,	26,	32,	35,	21,	50],
 [55,	53,	37,	32,	57,	52,	25,	37,	32,	53],
 [60,	44,	53,	54,	49,	27,	24,	40,	35,	28],
 [33,	30,	57,	33,	33,	55,	37,	25,	24,	34],
 [40,	56,	56,	27,	31,	44,	57,	53,	32,	51],
 [57,	49,	47,	39,	24,	46,	52,	47,	29,	34],
 [36,	54,42,	31,	21,	23,	24,	55,	48,	55],
 [22,	24,	60,	25,	43,	53,	33,	48,	28,	39],
 [59,	55,	24,	59,	31,	38,	51,	22,	30,	51],
 [59,	35,	28,	42,	23,	58,	49,	59,	36,	53],
 [48,	57,	35,	51,	47,	31,	40,	32,	56,	51],
 [49,	21,	47,	35,	53,	47,	40,	26,	32,	46]]
w = np.array(w)

Tt = \
[[0, 1, 1,	1,	1],
 [1, 0, 1,	1,	1],
 [1, 1, 0,	1,	1],
 [1, 1, 1,	0,	1],
 [1, 1, 1,	1,	0]]
Tt = np.array(Tt)

# 创建模型
mob = Model(name='mobile')

#变量设置
y = mob.binary_var_dict(range(M), name='Y')
x = mob.binary_var_dict([(j,m,t) for j in range(J) for m in range(M) for t in range(T)], name='X')
z = mob.binary_var_dict([(i,j,m,t) for i in range(I) for j in range(J) for m in range(M) for t in range(T)], name='Z')

#添加目标函数
f1 = mob.sum(f*y[m] for m in range(M))
f2 = mob.sum(a*x[j,m,t] for j in range(J) for m in range(M) for t in range(T))
f3 = mob.sum(b*d[i,j]*z[i,j,m,t] for i in range(I) for j in range(J) for m in range(M) for t in range(T))       
mob.minimize(f1 + f2 + f3)

#添加约束条件
mob.add_constraints(x[j,m,t] + x[jp,m,tp] <= y[m]
                    for j in range(J) 
                    for m in range(M)
                    for t in range(T)
                    for jp in list(set(range(J)).difference({j}))
                    for tp in range(t,min(t+Tt[j][jp],T)))
                
mob.add_constraints(mob.sum(z[i,j,m,t] for j in range(J) for m in range(M)) == 1
                    for i in range(I)
                    for t in range(T))

mob.add_constraints(mob.sum(w[i][t]*z[i,j,m,t] for i in range(I)) <= c*x[j,m,t]
                    for j in range(J)
                    for m in range(M)
                    for t in range(T))

# 求解 
mob.print_information()
mob.export_as_lp('mobile.lp')
#url='https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/'
#key='api_6d433c14-5a73-4d9f-8364-ec787ca576d9'
#sol = mob.solve(url=url, key=key)
mob.solve(log_output=True)
#mob.report()
mob.print_solution()









