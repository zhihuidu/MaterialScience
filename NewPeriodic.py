import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys
import random
#we will first sort the elements based on how many other elements can share it and especially the benefit
#This is also a heuristic algorithm. However, it consider how many elements can be shared by others.

def Higher_Weight_Edge(Finished,ToRun):
	High_candidate=[]
	Low_candidate=[]
	for i in ToRun:
		for j in Finished:
                	if d1.values[i][j]==2:
				High_candidate.append([j,i])
                	if d1.values[i][j]==1:
				Low_candidate.append([j,i])

	if len(High_candidate)>0:
		pair=High_candidate[int(random.uniform(0,len(High_candidate)-1))]
#		print "There are ",len(High_candidate), "High candidate and I select ", int(random.uniform(0,len(High_candidate)-1)), "It is ", pair[0],"->",pair[1]
        	Sequence=pair
		selectedrow=pair[1]
		selectedcol=pair[0]
		Sequence.append(d2.values[selectedrow][selectedcol+1])
		Sequence.append(d2.values[selectedrow][0]-d2.values[selectedrow][selectedcol+1])

	else:

		if len(Low_candidate)>0:
			pair=Low_candidate[int(random.uniform(0,len(Low_candidate)-1))]
#			print "There are ",len(Low_candidate), "low candidate and I select ",  int(random.uniform(0,len(Low_candidate)-1)),"It is", pair[0],"-",pair[1]
        		Sequence=pair
			selectedrow=pair[1]
			selectedcol=pair[0]
			Sequence.append(d2.values[selectedrow][selectedcol+1])
			Sequence.append(d2.values[selectedrow][0]-d2.values[selectedrow][selectedcol+1])
		else:
			SelectEle=ToRun[0]
#			print "No shared edge and I select the first queue element", SelectEle
        		Sequence=[SelectEle,SelectEle]
	        	Sequence.append(d2.values[SelectEle][0])
	        	Sequence.append(0.0)

	return Sequence




def Next_Best(Finished,ToRun):
	retseq=Higher_Weight_Edge(Finished,ToRun) #select one from ToRun who has a very high edge from Finished to ToRun
	return retseq



if len(sys.argv) < 2:
	print "arg error:\nusage: \tpython Heuristic-Information-File Execution-Time-file"

fn1 = sys.argv[1]
d1 = pd.read_csv(fn1, sep=" +",engine='python',header=None)
fn2 = sys.argv[2]
d2 = pd.read_csv(fn2, sep=" +",engine='python',header=None)
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']

SortAll=[]
HighQ=[]
LowQ=[]
for j in range(len(eleName)):
	HighNum=0
	LowNum=0
	High=[]
	Low=[]
        for i in range(len(eleName)):
                if d1.values[i][j] == 2 :
			HighNum=HighNum+1
			High.append(i)
                if d1.values[i][j] == 1 :
			LowNum=LowNum+1
			Low.append(i)
	HighQ.append(High)
	LowQ.append(Low)
	SortEle=[]
	SortEle.append(j)
	SortEle.append(HighNum)
	SortEle.append(LowNum)
	SortEle.append(eleName[j])
	SortAll.append(SortEle)

#print SortAll
NewSortAll=sorted(SortAll, key=lambda x:(x[1],x[2]), reverse=True)

#print NewSortAll
#print "HighQ=",HighQ

OriginalTotalTime=0.0
for i in range(len(eleName)):
	OriginalTotalTime=OriginalTotalTime+d2.values[i][0]

MinTime=9999999.99
AvgTime=0.0
IteNum=0
AllSchedule=[]
AllSequence=[]
for cur in range(len(eleName)):
	i=NewSortAll[cur][0]
	if NewSortAll[i][1]>0:
		totaltime=0.0
		Finished=[i]
		Sequence=[i,i] #Scheduling sequence
		Sequence.append(d2.values[i][0]) #Execute time
		Sequence.append(0.0) # Saved time
		ToRun=[]
		for k in range(len(eleName)):
			ToRun.append(NewSortAll[k][0])
		ToRun.remove(i)
		while len(ToRun)>0:
			retseq=Next_Best(Finished,ToRun)
			Sequence.append(retseq[0])
			Sequence.append(retseq[1])
			Sequence.append(retseq[2])
			Sequence.append(retseq[3])
			Finished.append(retseq[1])
			ToRun.remove(retseq[1])

		OnceSchedule=[]
		for j in range(len(eleName)):
#			print eleName[Sequence[j*3]],"->",eleName[Sequence[j*3+1]], "Execution Time=",Sequence[j*3+2]
			OnceSchedule.append( eleName[Sequence[j*4]] + "->" + eleName[Sequence[j*4+1]] +" " + str(Sequence[j*4+2])+" " + str(Sequence[j*4+3]) )
			totaltime=totaltime+Sequence[j*4+2]
		AvgTime=AvgTime+totaltime
		IteNum=IteNum+1
                AllSchedule.append(OnceSchedule)
                AllSequence.append(Sequence)
	#	print "Total Time=", totaltime
	#	print OnceSchedule 
		if totaltime<MinTime:
			MinTime=totaltime
			BestSchedule=OnceSchedule
AvgTime=AvgTime/IteNum
AveMin=99999999.0
for cur in range(len(AllSchedule)):
    totaltime=0.0
    for j in range(len(eleName)):
        totaltime=totaltime+Sequence[j*4+2]
    if abs(totaltime-AvgTime)<AveMin:
        AvgSchedule=AllSchedule[cur]

print " "
print "-------------Begin-----------"
print "Qualitative Description= ",fn1," Scheduling Result for Input Case:",fn2, "Iteration num=",IteNum


#print "Best Execution Time=",MinTime," Original Time=", OriginalTotalTime, "Saved Absolute Time=",OriginalTotalTime-MinTime, "Saved Relative Time=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime
#print "Average Execution Time=",AvgTime, "Average Saving Time=",OriginalTotalTime-AvgTime,"Relative Saving Time=",(OriginalTotalTime-AvgTime)/OriginalTotalTime

print "Execution Time, Original Time, Saved Absolute Time,Saved Relative Time"
print "E=",MinTime," O=", OriginalTotalTime, "A=",OriginalTotalTime-MinTime, "R=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime



OutPutSchedule=BestSchedule
for i in range(len(OutPutSchedule)):
        print OutPutSchedule[i]


print "Average Execution Time,  OriginalTotalTime, Average Saving Time,Relative Saving Time"
print "AE=",AvgTime, " AO=",  OriginalTotalTime, "AS=",OriginalTotalTime-AvgTime,"AR=",(OriginalTotalTime-AvgTime)/OriginalTotalTime

OutPutSchedule=AvgSchedule
for i in range(len(OutPutSchedule)):
        print OutPutSchedule[i]

print "-------------End-----------"

