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
def Get_Precedencessor(InputSchedule,i):
	RetSet=[]
	if InputSchedule[i][0]==InputSchedule[i][1]: #no precedencessor, so return itself
		RetSet=[InputSchedule[i][1]]
		return RetSet
	else:
		j=i-1
		while (InputSchedule[j][1] <> InputSchedule[i][0]) and j>=0: # find the precedencessor of the  ith schedule
			j=j-1
		TmpSet=Get_Precedencessor(InputSchedule,j)
		RetSet=RetSet+TmpSet
		RetSet.append(InputSchedule[i][1])
	return RetSet

def Check_Before(InputSchedule,MidEle,TmpEle):
#	print "Enter Check Before, The input schedule is", InputSchedule, "The midele is", MidEle
	PreSeq=[]
	i=0
	while InputSchedule[i][1] <> MidEle:
		PreSeq.append(copy.deepcopy(InputSchedule[i]))
		i=i+1
	if InputSchedule[i][1] == MidEle:
		PreSeq.append(copy.deepcopy(InputSchedule[i]))
#	print "The schedule before elemet ",MidEle," is ",PreSeq
	PrecedencessorSet=Get_Precedencessor(InputSchedule,i)
#	print "the elements before element=",MidEle, "are", PrecedencessorSet
	RemovedSeq=[]
	for i in PreSeq:
		if not (i[1] in PrecedencessorSet) :
			if  i[2] > d.values[i[1]][TmpEle+1]:
				i[2]=d.values[i[1]][TmpEle+1]
				i[3]=d.values[i[1]][0]- d.values[i[1]][TmpEle+1]
				i[0]=TmpEle
			RemovedSeq.append(copy.deepcopy(i))
			#PreSeq.remove(i) this will cause error, jump to next element
	for i in RemovedSeq:
		PreSeq.remove(i)
        for i in range(len(PreSeq)-1):
                PreSeq[i+1][4]=PreSeq[i][4]+PreSeq[i+1][2]

#	print "I will keep " ,PreSeq, "and remove ", RemovedSeq
#	print "Leave Check Before"
	RetSeq=[PreSeq,RemovedSeq]	
	return RetSeq

def Check_After(InputSchedule,MidEle,TmpEle):
	RetSeq=[]
	for i in range(len(InputSchedule)):
		if InputSchedule[i][1] == MidEle:
			for j in range(i+1,len(InputSchedule)):
				TmpSeq=copy.deepcopy(InputSchedule[j])
				if TmpSeq[2] > d.values[TmpSeq[1]][TmpEle+1]:
					TmpSeq[2]=d.values[TmpSeq[1]][TmpEle+1]
					TmpSeq[3]=d.values[TmpSeq[1]][0]- d.values[TmpSeq[1]][TmpEle+1]
					TmpSeq[0]=TmpEle

				RetSeq.append(TmpSeq)
			return RetSeq


def At_Mid(EleSet,MidSchedule,TmpEle):  #EleSet is the set which has the best schedule EndSchedule, tmpEle is the element to be added into the middle.
#I will change MidSchedule directly but do not change EleSet
#	print "Enter At Mid"
	MyTime=d.values[TmpEle][0]
	TmpTime=MyTime
	UsedEle=TmpEle
	DiffSchedules=[]
	for i in EleSet:
		if d.values[TmpEle][i+1] <MyTime:
#			print " I find an element ",i, "can reduce the execution of element ",TmpEle
			FirstCheck=Check_Before(MidSchedule,i,TmpEle)
			FirstPart=FirstCheck[0]
			AccumulatedTime=FirstPart[-1][4]
			SecondPart=Check_After(MidSchedule,i,TmpEle)
			CurSeq=[i,TmpEle,d.values[TmpEle][i+1],MyTime-d.values[TmpEle][i+1],AccumulatedTime+d.values[TmpEle][i+1]]
			FirstPart.append(CurSeq)
#			print "-----------"
#			print "First part=", FirstPart
#			print "Removed part=", FirstCheck[1]
#			print "-----------"
			FirstPart=FirstPart+FirstCheck[1]
			ret=FirstPart	
			if len(SecondPart)>0:
				ret=FirstPart+SecondPart
			for i in range(len(ret)-1):
				ret[i+1][4]=ret[i][4]+ret[i+1][2]
			DiffSchedules.append(ret)
	ExeTime=99999999.9
	SchId=-1
	for i in range(len(DiffSchedules)):
		if DiffSchedules[i][-1][4]<ExeTime:
			ExeTime=DiffSchedules[i][-1][4]
			SchId=i
	if SchId <> -1:
		RetSeq=DiffSchedules[SchId]
	else:
		RetSeq=[]
#	print "Before leave At_Mid ret=",RetSeq
	return RetSeq
def At_End(EleSet,EndSchedule,TmpEle):  #EleSet is the set which has the best schedule EndSchedule, tmpEle is the element to be added at the end. 
#I will change EndSchedule directly but do not change EleSet
#def At_End(EndElementstmpElements,tmpSmallSeq,tmpOneEle):  #EndElements is the set which has the best schedule EndSchedule
#	print "Enter At End"
	MyTime=d.values[TmpEle][0]
	TmpTime=MyTime
	UsedEle=TmpEle
	for i in EleSet:
		if d.values[TmpEle][i+1] <TmpTime:
			TmpTime=d.values[TmpEle][i+1]
			UsedEle=i
	LastSeqNum=len(EndSchedule)-1
	AccumulatedTime=TmpTime+EndSchedule[-1][4]
	TmpSeq=[UsedEle,TmpEle,TmpTime,MyTime-TmpTime,AccumulatedTime]	
	EndSchedule.append(TmpSeq)
	ret=EndSchedule
#	print "Before leave At_End ret=",ret
	return ret

def At_First(EleSet,FirstSchedule,TmpEle): # EleSet is the set which has the best schedule FirstSchedule, TmpEle is the element to be added at the head
#def At_First(Elements,SmallSeq,OneEle):
#	print "Enter At First"
	MyTime=d.values[TmpEle][0]
	TmpTime=MyTime
	UseEle=TmpEle
	for i in range(len(FirstSchedule)):
		if FirstSchedule[i][2]>d.values[FirstSchedule[i][1]][TmpEle+1]:
			FirstSchedule[i][2]=d.values[FirstSchedule[i][1]][TmpEle+1]
			FirstSchedule[i][0]=TmpEle
			FirstSchedule[i][3]=d.values[FirstSchedule[i][1]][0]-d.values[FirstSchedule[i][1]][TmpEle+1]
	HeadEle=[[TmpEle,TmpEle,MyTime,0,MyTime]]
	ret=HeadEle+FirstSchedule
	for i in range(len(ret)-1):
		ret[i+1][4]=ret[i][4]+ret[i+1][2]
#	print "Before leave At_First ret=",ret
	return ret
		
def Recursive_Schedule(Elements):
#	print "Enter Recursive"
	if len(Elements)<=0:
		print "Error in Elements List"
		return 0
	if len(Elements) ==1 :
		FirstEle=Elements[0]
		Sequence=[[FirstEle,FirstEle,d.values[FirstEle][0],0.0,d.values[FirstEle][0]]]
		return Sequence
	if len(Elements) ==2 :
#		print "When Elements have two"
		FirstEle=Elements[0]
		SecondEle=Elements[1]
		FirstTime=d.values[FirstEle][0]
		SecondTime=d.values[SecondEle][0]
		ViaSecondTime=d.values[FirstEle][SecondEle]
		ViaFirstTime=d.values[SecondEle][FirstEle]

		if ViaFirstTime<SecondTime or ViaSecondTime<FirstTime :# sharing is better
			if FirstTime+ViaFirstTime<SecondTime+ViaSecondTime:
				Seq1=[[FirstEle,FirstEle,FirstTime,0.0,FirstTime]]
				Seq2=[FirstEle,SecondEle,ViaFirstTime,SecondTime-ViaFirstTime,FirstTime+ViaFirstTime]
				Seq1.append(Seq2)
			else:
				Seq1=[[SecondEle,SecondEle,SecondTime,0.0,SecondTime]]
				Seq2=[SecondEle,FirstEle,ViaSecondTime,FirstTime-ViaSecondTime,SecondTime+ViaSecondTime]
				Seq1.append(Seq2)
		else:
			Seq1=[[FirstEle,FirstEle,FirstTime,0.0,FirstTime]]
			Seq2=[SecondEle,SecondEle,SecondTime,0.0,FirstTime+SecondTime]
			Seq1.append(Seq2)
#		print "Before leave Recursive ret=",Seq1
		return Seq1
	elif len(Elements) >=3:
		tmpElements=copy.deepcopy(Elements)
		ExeTime=0
		for i in Elements: # remove the element which need the longest time
			if d.values[i][0]>ExeTime:
				ExeTime=d.values[i][0]
				OneEle=i
		tmpElements.remove(OneEle)
#		print "Before enter recursive with less Elements=",tmpElements
		CurSmallSeq=Recursive_Schedule(tmpElements)
#		print "Out from recursive with less Elements, the schedule=",CurSmallSeq
		forAtFirstSeq=copy.deepcopy(CurSmallSeq)
		FirstRunSeq=At_First(tmpElements,forAtFirstSeq,OneEle)
#		print "At First Result ",FirstRunSeq
		forAtEndSeq=copy.deepcopy(CurSmallSeq)
		EndRunSeq=At_End(tmpElements,forAtEndSeq,OneEle)
#		print "At End Result ",EndRunSeq
		forAtMidSeq=copy.deepcopy(CurSmallSeq)
		MidRunSeq=At_Mid(tmpElements,forAtMidSeq,OneEle)
#		print "Mid Run Result=",MidRunSeq
		retseq=FirstRunSeq
		if len(MidRunSeq)>0:
			if FirstRunSeq[-1][4] >MidRunSeq[-1][4]:
				retseq=MidRunSeq
		if retseq[-1][4]>EndRunSeq[-1][4]:
			retseq=EndRunSeq
		return retseq

#######################
####################### End of the function
#######################

IteNum=1
AverageTime=[0.0,0.0,0.0,0.0]
for loop in range(IteNum):

    OriginalTotalTime=0.0
    for i in range(len(eleName)):
    	OriginalTotalTime=OriginalTotalTime+d.values[i][0]

    ToRun=range(0,19)
    BestSchedule=Recursive_Schedule(ToRun)

    OriginalTotalTime=0.0
    for i in range(len(eleName)):
    	OriginalTotalTime=OriginalTotalTime+d_bak.values[i][0]

    Cur_Ele=BestSchedule[0][0]
    BestSchedule[0][4]=d_bak.values[Cur_Ele][0]
    BestSchedule[0][2]=d_bak.values[Cur_Ele][2]
    BestSchedule[0][1]=Cur_Ele
    BestSchedule[0][3]=0.0
    for i in range(1,19):
    	From_Ele=BestSchedule[i][0]
    	To_Ele=BestSchedule[i][1]
    	BestSchedule[i][2]=d_bak.values[To_Ele][From_Ele+1]
    	BestSchedule[i][3]=d_bak.values[To_Ele][0]-d_bak.values[To_Ele][From_Ele+1]
    	BestSchedule[i][4]=BestSchedule[i-1][4] + d_bak.values[To_Ele][From_Ele+1]


    MinTime=BestSchedule[-1][4]
    OutPutSchedule=[]
    for j in range(len(eleName)):
    	OutPutSchedule.append( eleName[BestSchedule[j][0]] + "->" + eleName[BestSchedule[j][1]] +" " + str(BestSchedule[j][2])+" "+str(BestSchedule[j][3])+" "+str(BestSchedule[j][4]) )
    	Lines=[]
    	Lines.append("%5d"%(BestSchedule[j][0]))
    	Lines.append("%5d"%(BestSchedule[j][1]))
    	Lines.append("%15.3f"%(BestSchedule[j][2]))
    	Lines.append("%15.3f"%(BestSchedule[j][3]))
    	Lines.append("%15.3f"%(BestSchedule[j][4]))
    	Lines.append("\r\n")
    	Outfile.writelines(Lines)
    AverageTime[0]=AverageTime[0]+MinTime
    AverageTime[1]=AverageTime[1]+OriginalTotalTime
    AverageTime[2]=AverageTime[2]+OriginalTotalTime-MinTime
    AverageTime[3]=AverageTime[3]+(OriginalTotalTime-MinTime)/OriginalTotalTime

AverageTime[0]=AverageTime[0]/IteNum
AverageTime[1]=AverageTime[1]/IteNum
AverageTime[2]=AverageTime[2]/IteNum
AverageTime[3]=AverageTime[3]/IteNum

print "-------------Begin-----------"
print "SmalltoBigHeuristicBest.py BigFile Heuristic-Information-File SmallFile "
#print "Execution Time=",MinTime," Original Time=", OriginalTotalTime, "Saved Absolute Time=",OriginalTotalTime-MinTime, "Saved Relative Time=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime

print "Average Execution Time, Original Time, Saved Absolute Time,Saved Relative Time"
#print "E=",MinTime," O=", OriginalTotalTime, "A=",OriginalTotalTime-MinTime, "R=" ,(OriginalTotalTime-MinTime)/OriginalTotalTime
print "E=",AverageTime[0]," O=", AverageTime[1], "A=",AverageTime[2], "R=" ,AverageTime[3]

print "Scheduling Result using small result in periodic table:"
print "The meaning of each element of the schedule is : "
print "E1->E2(E2 shares the result of E1), E2 Exe Time, E2 Saved Time, Accumulated Time"
for i in range(len(OutPutSchedule)):
	print OutPutSchedule[i]
#for i in BestSchedule:
#	print eleName[i[0]]+"->"+eleName[i[1]],i[2],i[3],i[4]
print "-------------End-------------"
Outfile.close()
