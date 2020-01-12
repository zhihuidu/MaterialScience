import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys

#05-20,2-10, In this script, we will read the qulitative description directly from keyboard. However, the digital number will describe the level, the larger, the better

if len(sys.argv) < 2:
	print "arg error:\nusage: \tpython Heuristic-Information-File oExecution-Time-file"
	exit(0)



 x = input('Input an integer: ')


fn1 = sys.argv[1]
d = pd.read_csv(fn1, sep=" +",engine='python',header=None)
#fn2 = sys.argv[2]
#fn = "energy_energy_bind.dat"
#fn = "energy_spin_energy_bind.dat"
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']


def Current_Min(Finished,ToRun,MaxVal):
	cur_min=MaxVal
	for i in ToRun:
		for j in Finished:
			if d.values[i][j+1] < cur_min:
				cur_min=d.values[i][j+1]
                        	Sequence=[j,i]
			if d.values[i][0] < cur_min:
				cur_min=d.values[i][0]
                        	Sequence=[i,i]
	Sequence.append(cur_min)
	return Sequence



def Reduce_More(Finished,ToRun,MinVal):
        cur_min=MinVal
        for i in ToRun:
                for j in Finished:
                        if d.values[i][0]- d.values[i][j+1] > cur_min:
                                cur_min=d.values[i][0]- d.values[i][j+1]
                                Sequence=[j,i]
                if cur_min<=0:
	                Sequence=[i,i]
	if Sequence[1]==Sequence[0]:
		Sequence.append(d.values[Sequence[1]][0])
	else:
        	Sequence.append(d.values[Sequence[1]][Sequence[0]+1])
        return Sequence

OriginalTotalTime=0.0
for i in range(len(eleName)):
	OriginalTotalTime=OriginalTotalTime+d.values[i][0]

MinTime=9999999.99
for i in range(len(eleName)):
	totaltime=0.0
	Finished=[i]
	Sequence=[i,i]
	Sequence.append(d.values[i][0])
	Sequence.append(0.0)
	ToRun=range(0,19)
	ToRun.remove(i)
	for j in range(len(eleName)-1):
		#retseq=Current_Min(Finished,ToRun,99999999.9)
		retseq=Reduce_More(Finished,ToRun,-1.0)
		Sequence.append(retseq[0])
		Sequence.append(retseq[1])
		Sequence.append(retseq[2])
		Sequence.append(d.values[retseq[1]][0]-retseq[2])
		Finished.append(retseq[1])
		ToRun.remove(retseq[1])

#	print "Schedule From element ",eleName[i]
	OnceSchedule=[]
	for j in range(len(eleName)):
#		print eleName[Sequence[j*3]],"->",eleName[Sequence[j*3+1]], "Execution Time=",Sequence[j*3+2]
		OnceSchedule.append( eleName[Sequence[j*4]] + "->" + eleName[Sequence[j*4+1]] +" " + str(Sequence[j*4+2])+" " + str(Sequence[j*4+3]) )
		totaltime=totaltime+Sequence[j*4+2]

#	print "Total Time=", totaltime
#	print OnceSchedule 
	if totaltime<MinTime:
		MinTime=totaltime
		BestSchedule=OnceSchedule


#AccumulatedTime=0.0
#OutPutSchedule=[]
#for j in range(len(eleName)):
#	AccumulatedTime=AccumulatedTime + BestSchedule[j*4+2]
#        OutPutSchedule.append( eleName[BestSchedule[j*4]] + "->" + eleName[BestSchedule[j*4+1]] +" " + str(BestSchedule[j*4+2])+" "+str(BestSchedule[j*4+3])+" "+str(AccumulatedTime))

print "-------------Begin-----------"
print "RMF (Reduced More First) Scheduling Result for Input Case:",fn1
print "Execution Time=",MinTime," Original Time=", OriginalTotalTime, "Saved Absolute Time=",OriginalTotalTime-MinTime, "Saved Relative Time=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime
print "Scheduling Result with RMF(Reduced More First) Policy:"
#print "The meaning of each element of the schedule is : E1->E2(E2 shares the result of E1), E2 Exe Time, E2 Saved Time, Accumulated Time"
print "The meaning of each element of the schedule is : E1->E2(E2 shares the result of E1), E2 Exe Time, E2 Saved Time"
print BestSchedule
print "-------------End-----------"

MinTime=9999999.99
for i in range(len(eleName)):
        totaltime=0.0
        Finished=[i]
        Sequence=[i,i]
        Sequence.append(d.values[i][0])
	Sequence.append(0.0)
        ToRun=range(0,19)
        ToRun.remove(i)
        for j in range(len(eleName)-1):
                retseq=Current_Min(Finished,ToRun,99999999.9)
                #retseq=Reduce_More(Finished,ToRun,0)
                Sequence.append(retseq[0])
                Sequence.append(retseq[1])
                Sequence.append(retseq[2])
		Sequence.append(d.values[retseq[1]][0]-retseq[2])
                Finished.append(retseq[1])
                ToRun.remove(retseq[1])

#       print "Schedule From element ",eleName[i]
        OnceSchedule=[]
        for j in range(len(eleName)):
#               print eleName[Sequence[j*3]],"->",eleName[Sequence[j*3+1]], "Execution Time=",Sequence[j*3+2]
		OnceSchedule.append( eleName[Sequence[j*4]] + "->" + eleName[Sequence[j*4+1]] +" " + str(Sequence[j*4+2])+" "+str(Sequence[j*4+3]) )
                totaltime=totaltime+Sequence[j*4+2]

#       print "Total Time=", totaltime
#       print OnceSchedule 
        if totaltime<MinTime:
                MinTime=totaltime
                BestSchedule=OnceSchedule
#AccumulatedTime=0.0
#OutPutSchedule=[]
#for j in range(len(eleName)):
#	AccumulatedTime=AccumulatedTime+BestSchedule[j*4+2]
#        OutPutSchedule.append( eleName[BestSchedule[j*4]] + "->" + eleName[BestSchedule[j*4+1]] +" " + str(BestSchedule[j*4+2])+" "+str(BestSchedule[j*4+3])+" "+str(AccumulatedTime))
print "-------------Begin-----------"
print "STF (Shortest Time First) Scheduling Result for Input Case:",fn1
print "Execution Time=",MinTime," Original Time=", OriginalTotalTime, "Saved Absolute Time=",OriginalTotalTime-MinTime, "Saved Relative Time=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime
print "Scheduling Result with STF(Shortest Time First) Policy:"
print "The meaning of each element of the schedule is : E1->E2(E2 shares the result of E1), E2 Exe Time, E2 Saved Time"
print BestSchedule
print "-------------End-------------"
