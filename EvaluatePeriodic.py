import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys
import random
#we will first sort the elements based on how many other elements can share it and especially the benefit
#This is also a heuristic algorithm. However, it consider how many elements can be shared by others.




if len(sys.argv) < 2:
	print "arg error:\nusage: \tpython  EvaluatePeriodic.py Heuristic-Information-File Execution-Time-file HighThreshold"

fn1 = sys.argv[1]
d1 = pd.read_csv(fn1, sep=" +",engine='python',header=None)
fn2 = sys.argv[2]
d2 = pd.read_csv(fn2, sep=" +",engine='python',header=None)
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']

HighThreshold=float(sys.argv[3])
#-0.35
ExactSame=0.0
HighAsLow=0.0
LowAsHigh=0.0
Wrong=0.0
HighValue=0.0
LowValue=0.0
BaselineAveExecutionTime=0.0
MinExecutionTime=np.min(d2.values)
MaxExecutionTime=np.max(d2.values)
AveExecutionTime=np.mean(d2.values)
BaselineAveExecutionTime=0.0
for j in range(len(eleName)):
    BaselineAveExecutionTime=BaselineAveExecutionTime+d2.values[j][0]
BaselineAveExecutionTime=BaselineAveExecutionTime/19.0
#print "File=",sys.argv[2],"Min Execution Time=",MinExecutionTime,"Max Execution Time=",MaxExecutionTime,"Average Execution Time=",AveExecutionTime,"Baseline Average Execution Time=",BaselineAveExecutionTime
#exit(0)
EmptyValue=0.0
HighList=[]
LowList=[]
EmptyList=[]
HighNum=0.0
LowNum=0.0
TP=0.0
FN=0.0
FP=0.0
TN=0.0
for j in range(len(eleName)):
        for i in range(len(eleName)):
                if i==j:
                    continue
                if d1.values[i][j] == 2 :
                        HighValue=HighValue+(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]
                        HighList.append((d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0])

#print "File=",sys.argv[2],"Min Execution Time=",MinExecutionTime,"Max Execution Time=",MaxExecutionTime
#exit(0)
'''
AveExecutionTime=np.mean(d2.values)
#print "File=",sys.argv[2],"Average Execution Time=",AveExecutionTime
#exit(0)
for j in range(len(eleName)):
    AveExecutionTime=AveExecutionTime+d2.values[j][0]
AveExecutionTime=AveExecutionTime/19.0
print "File=",sys.argv[2],"Average Execution Time=",AveExecutionTime
exit(0)
'''
ExactSame=0.0
HighAsLow=0.0
LowAsHigh=0.0
Wrong=0.0
EmptyValue=0.0
EmptyList=[]
HighValue=0.0
HighList=[]
LowValue=0.0
LowList=[]
HighNum=0.0
LowNum=0.0
TP=0.0
FN=0.0
FP=0.0
TN=0.0
for j in range(len(eleName)):
        for i in range(len(eleName)):
                if i==j:
                    continue
                if d1.values[i][j] == 2 :
                        HighValue=HighValue+(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]
                        HighList.append((d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0])
                        HighNum=HighNum+1
                        if (d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0] <= HighThreshold:
                            ExactSame=ExactSame+1
                            TP=TP+1
                        else:
                            if (d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]<0.0:
                                LowAsHigh=LowAsHigh+1
                                TP=TP+1
                            else:
                                Wrong=Wrong+1
                                FP=FP+1
                elif d1.values[i][j] == 1 :
                        LowValue=LowValue+(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]
                        LowList.append((d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0])
                        LowNum=LowNum+1
                        if (d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0] <= HighThreshold:
                            HighAsLow=HighAsLow+1
                            TP=TP+1
                        else:
                            if (d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]<0:
                                ExactSame=ExactSame+1
                                TP=TP+1
                            else:
                                Wrong=Wrong+1
                                FP=FP+1
                else:
                        if (d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0] < 0.0:
                           FN=FN+1
                        else:
                           TN=TN+1
                        EmptyList.append((d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0])
                        EmptyValue=EmptyValue+(d2.values[i][j+1]-d2.values[i][0])/d2.values[i][0]

Correct=HighAsLow+LowAsHigh+ExactSame
Total=Correct+Wrong+0.0
PerCentSame=ExactSame/Total
PerCentHighAsLow=HighAsLow/Total
PerCentLowAsHigh=LowAsHigh/Total
PerCentCorrect=Correct/Total
PerCentWrong=Wrong/Total
AverageHigh=HighValue/HighNum
AverageLow=LowValue/LowNum

Accuracy=(TP+TN)/(TP+TN+FP+FN)
Precision=(TP)/(TP+FP)
Recall=(TP)/(TP+FN)
EmptyPercentage=np.mean(np.array(EmptyList))*(-1)
#print EmptyValue/(len(EmptyList)*(-1.0))

#print sys.argv[2],"Exact Same", "High As Low", "Low As High", "Correct", "Wrong","Total" 
#print "%s %.2f   %.2f  %.2f  %.2f  %.2f  %.2f" %(sys.argv[2],HighThreshold,PerCentSame,PerCentHighAsLow,PerCentLowAsHigh,PerCentCorrect,PerCentWrong)

#print(' {0:2.0f}\%  & {1:2.0f}\%  & {2:2.0f}\%  & {3:2.0f}\%  & {4:2.0f}\%  & {5:2.0f}\%\\\\'.format(HighThreshold*100.0*(-1),PerCentSame*100.0, PerCentHighAsLow*100,PerCentLowAsHigh*100,PerCentCorrect*100,PerCentWrong*100))

print(' &  & {0:2.0f}\%  & {1:2.0f}\%  & {2:2.0f}\%   & {3:2.0f}\%  & {4:2.0f}\%  \\\\'.format(AverageHigh*100.0*(-1),AverageLow*100.0*(-1),EmptyPercentage*100,Precision*100,Recall*100))

#print(' &  & {0:2.0f}\%  & {1:2.0f}\%  & {2:2.0f}\%   & {3:2.0f}\%  & {4:2.0f}\%   & {5:2.0f}\%  \\\\'.format(AverageHigh*100.0*(-1),AverageLow*100.0*(-1),Precision*100,PerCentWrong*100,Accuracy*100,Recall*100))

#print "%s %.2f   %.2f  %.2f  %.2f %.2f  %.2f  %.2f  %.2f" %(sys.argv[2],HighThreshold,AverageHigh,AverageLow,PerCentSame,PerCentHighAsLow,PerCentLowAsHigh,PerCentCorrect,PerCentWrong)
#print "%s %.2f   %.2f  %.2f  %.2f %.2f  %.2f  %.2f   " %(sys.argv[2],AverageHigh,AverageLow,PerCentCorrect,Precision, Accuracy,Recall, PerCentWrong)


#print "High Average=", np.mean(HighList), "High Var=",np.var(HighList),"Low Average=",np.mean(LowList),"Low Var=",np.var(LowList)
