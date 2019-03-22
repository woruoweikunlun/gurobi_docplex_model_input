# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 21:46:44 2019
@author: Chengyi.zhang
"""

from gurobipy import *
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

mob = Model('mobile')

##变量设置           
y = mob.addVars(range(M), lb=0, ub=1, vtype=GRB.BINARY, name='Y')
x = mob.addVars([(j,m,t) for j in range(J) for m in range(M) for t in range(T)], lb=0, ub=1, vtype=GRB.BINARY, name='X')
z = mob.addVars([(i,j,m,t) for i in range(I) for j in range(J) for m in range(M) for t in range(T)], lb=0, ub=1, vtype=GRB.BINARY, name='Z')

mob.update()

##添加目标函数
f1 = quicksum(f*y[m] for m in range(M))
f2 = quicksum(a*x[j,m,t] for j in range(J) for m in range(M) for t in range(T))
f3 = quicksum(b*d[i,j]*z[i,j,m,t] for i in range(I) for j in range(J) for m in range(M) for t in range(T))       
mob.setObjective(f1+f2+f3, GRB.MINIMIZE)

##添加约束条件
mob.addConstrs(x[j,m,t] + x[jp,m,tp] <= y[m]
               for j in range(J) 
               for m in range(M)
               for t in range(T)
               for jp in list(set(range(J)).difference({j}))
               for tp in range(t,min(t+Tt[j][jp],T)))
                
mob.addConstrs(quicksum(z[i,j,m,t] for j in range(J) for m in range(M)) == 1
               for i in range(I)
               for t in range(T))

mob.addConstrs(quicksum(w[i][t]*z[i,j,m,t] for i in range(I)) <= c*x[j,m,t]
               for j in range(J)
               for m in range(M)
               for t in range(T))

#输出求解结果
def printSolution():
    if mob.status == GRB.Status.OPTIMAL:
        print('optimal value: %d'%mob.objVal)
        for m in range(M):
            if (y[m].x>0.0001):
                print('y[%d]=%d'%(m+1,y[m].x))
        for j in range(J):
            for m in range(M):
                for t in range(T):
                    if (x[j,m,t].x>0.0001):
                        print('x[%d,%d,%d]=%d'%(j+1,m+1,t+1,x[j,m,t].x))
        for i in range(I):
            for j in range(J):
                for m in range(M):
                    for t in range(T):
                        if (z[i,j,m,t].x>0.0001):
                            print('z[%d,%d,%d,%d]=%d'%(i+1,j+1,m+1,t+1,z[i,j,m,t].x))
    else:
        print('No Solution')

#求解 
mob.write('mobile.lp')
mob.optimize()
printSolution()










