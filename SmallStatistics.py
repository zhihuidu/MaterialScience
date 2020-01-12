import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys
import copy
import random

#fn2 = sys.argv[2]
#fn = "energy_energy_bind.dat"
#fn = "energy_spin_energy_bind.dat"
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']

'''
if len(sys.argv) < 2:
	print "arg error:\nusage: \tpython SmalltoBigHeuristicBest.py BigFile Heuristic-Information-File SmallFile"
	exit(0)

fn1 = sys.argv[1]

noise = 0.0
d = pd.read_csv(fn1, sep=" +",engine='python',header=None)
d_bak=copy.deepcopy(d)


fn2 = sys.argv[2]
d2 = pd.read_csv(fn2, sep=" +",engine='python',header=None)
fn3 = sys.argv[3]
d3 = pd.read_csv(fn3, sep=" +",engine='python',header=None)


for j in range(len(eleName)):
        for i in range(len(eleName)):
            d.values[i][j]=d3.values[i][j]
            d.values[i][j+1]=d3.values[i][j+1]
            if d2.values[i][j] == 0 :
                d.values[i][j+1]=9999999.99


Outfile=open(fn1[0:-4]+"Best-Check.txt","w")
'''


print "-------------End-------------"
Outfile.close()
