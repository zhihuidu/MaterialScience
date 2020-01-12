import string
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys
import random
from scipy import stats
from scipy.stats import t
#we will first sort the elements based on how many other elements can share it and especially the benefit
#This is also a heuristic algorithm. However, it consider how many elements can be shared by others.


import numpy as np
import matplotlib.pyplot as plt

def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return(b_0, b_1)

def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s =30)

    # predicted response vector
    y_pred = b[0] + b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color = "g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()

def main():
    # observations
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

    # estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))

    # plotting regression line
    plot_regression_line(x, y, b)



'''
if len(sys.argv) < 2:
	print "arg error:\nusage: \tpython  SmallResultFile BigResultFile Heuristic-File"

fn1 = sys.argv[1]
d1 = pd.read_csv(fn1, sep=" +",engine='python',header=None)
fn2 = sys.argv[2]
d2 = pd.read_csv(fn2, sep=" +",engine='python',header=None)
fn3 = sys.argv[3]
d3 = pd.read_csv(fn3, sep=" +",engine='python',header=None)
Inputfile1=file(fn1[0:-4]+"Best-Check.txt")
'''

Heuristic=[0.41,0.51,0.3,0.6,0.34,0.13,0.23,0.66]
Optimal=[0.52,0.69,0.48,0.71,0.68,0.29,0.65,0.89]

Better=np.array(Optimal)-np.array(Heuristic)

mean=np.mean(Better)
var=np.var(Better)
std=np.std(Better)

print "Mean=",mean, "var=", var, "Std=", std

'''
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']

for j in range(len(eleName)):
#        i=int(random.uniform(0,len(eleName)-1))
    for i in range(len(eleName)):
        if d3.values[i][j]<>0:
            SmallSavedPercent=(d1.values[i][j+1]-d1.values[i][0])/d1.values[i][0]
            BigSavedPercent=(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]
            SmallQ.append(SmallSavedPercent)
            BigQ.append(BigSavedPercent)

'''
'''
print SmallQ
print
print
print BigQ
'''

'''
ab=np.array([SmallQ,BigQ])
x=np.corrcoef(ab)
print "x=",x[1][0]

x = np.array(SmallQ)*(-1)
y = np.array(BigQ)*(-1)
ab=np.array([SmallQ,BigQ])
ar=np.corrcoef(ab)
r=ar[1][0]
tval=r*np.sqrt(len(SmallQ)-2)/np.sqrt(1-r*r)
pvalue=t.pdf(tval,len(SmallQ)-2)
print "corelation coefficient=",r,"tvalue=",tval,"pvalue=",pvalue,"freedom=",len(SmallQ)-2
b = estimate_coef(x, y)
plot_regression_line(x, y, b)
y_pred = b[0] + b[1]*x
diffy=abs(y-y_pred)
print "Small System", max(SmallQ),min(SmallQ)
print SmallQ
print "Big System",max(BigQ),min(BigQ)
print BigQ
plt.plot(range(0,64,1),y_pred,color='r',linestyle="--",marker="*",linewidth=2.0,label="Prediction")
plt.plot(range(0,64,1),y,color='k',linestyle="-",marker="o",linewidth=1.0,label="Big MPS")
plt.plot(range(0,64,1),x,color='g',linestyle=":",marker="+",linewidth=1.0,label="Small MPS")
plt.xlabel('Sampling Point')
plt.ylabel('Time Saving Percentage')
plt.legend(loc='lower right')
#plt.title("Comparison")
plt.savefig("Prediction.png",dpi=120)
plt.show()


mean=np.mean(diffy)
var=np.var(diffy)
print "mean=",mean,"var=",var
print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))
# plotting regression line
#plot_regression_line(x, y, b)

Num=32
for i in range(0,10):
    partx=SmallQ[i:i+32]
    party=BigQ[i:i+32]
    ab=np.array([partx,party])
    c=np.corrcoef(ab)
    tvalue=c[1][0]/np.sqrt((1-c[1][0]*c[1][0])/30)
    print "i=",i,"c=",c[1][0],"n=30,t=",tvalue


t_result=stats.ttest_ind(x,y,equal_var=False)
print t_result

t_result=stats.ttest_rel(x,y)
print t_result
'''
'''
g_s_m = pd.Series(SmallQ)
g_a_d = pd.Series(BigQ)

corr_gust = round(g_s_m.corr(g_a_d), 4)
print "corr=",corr_gust
'''

'''
SmallQ=[ 0.52657769735354, 0.389878831076265, 0.480843346180005, 0.644440270473328, 0.617608120035305, 0.505090748118637, 0.544402314907204, 0.603986461075592, 0.56651908075058, 0.577601947656726, 0.52602875557759, 0.599794661190965, 0.651649746192893, 0.519514884233738, 0.592944708531399, 0.458131655372701, 0.453462397617275, 0.476962858486131]
BigQ=[0.6141992638343, 0.413650732210825, 0.460204941044357, 0.503376002250668, 0.596844509030517, 0.56041388518024, 0.585902565309485, 0.653453101607759, 0.443896608396833, 0.553976102183766, 0.625923047026817, 0.671917474036384, 0.657791806765937, 0.805305241781952, 0.587646180641951, 0.728236027425722, 0.357520683575207, 0.49433883142298]

ab=np.array([SmallQ,BigQ])
x=np.corrcoef(ab)
print "x=",x[1][0]

ab=np.array([SmallQ,BigQ])
x=np.corrcoef(ab)
print "x=",x[1][0]

x = np.array(SmallQ)
y = np.array(BigQ)
b = estimate_coef(x, y)
print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))
# plotting regression line
#plot_regression_line(x, y, b)
'''

'''
plt.scatter(SmallQ,BigQ)
plt.show()
'''

'''
The following codes are used to get the results from scheduling output
for eachline in Inputfile1:
#    print eachline
    j=int(eachline[0:6])
    i=int(eachline[7:11])
    if i==j:
        continue
    SmallSavedPercent=(d1.values[i][j+1]-d1.values[i][0])/d1.values[i][0]
    BigSavedPercent=(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]
    SmallQ.append(SmallSavedPercent)
    BigQ.append(BigSavedPercent)
 #  print SmallSavedPercent, BigSavedPercent
'''
