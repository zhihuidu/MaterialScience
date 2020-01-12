import pandas as pd
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import sys

from matplotlib.pyplot import figure, show, rc


#from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

datafile = cbook.get_sample_data('aapl.csv', asfileobj=False)
print ('loading %s' % datafile)
r = mlab.csv2rec(datafile)

r.sort()
r = r[-30:]  # get the last 30 days


# first we'll do it the default way, with gaps on weekends
fig, ax = plt.subplots()
ax.plot(r.date, r.adj_close, 'o-')
fig.autofmt_xdate()

# next we'll write a custom formatter
N = len(r)
ind = np.arange(N)  # the evenly spaced plot indices

def format_date(x, pos=None):
    thisind = np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime('%Y-%m-%d')

fig, ax = plt.subplots()
ax.plot(ind, r.adj_close, 'o-')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()

plt.show()

exit(0)


if len(sys.argv) < 1:
	print "arg error:\nusage: \tpython Radar.py input-data-fiel"
	exit(0)

zero_relative = float(sys.argv[3])
fn = sys.argv[1]
#fn = "energy_energy_bind.dat"
#fn = "energy_spin_energy_bind.dat"
#eleName = ['Al','Sc','Ti','V','Cr','Mn','Fe','Co','Cu','Zn','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','Hf','Ta','W','Re','Os','Ir','Pt','Au']
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']
eleName1 = ['Ti','V','Cr','Mn','Fe','Co','Ni']
eleName2 = ['Zr','Nb','Mo','Tc','Ru','Rh','Pd']
eleName3 = ['Hf','Ta','W','Re','Os','Ir','Pt']
 
ZeroL=[]
HalfL=[]
QuarterL=[]
MHalfL=[]
MQuarterL=[]
transparantVal=0.7
#d=pd.read_csv(fn)
d = pd.read_csv(fn, sep=" +",engine='python',header=None)
#print d.values[0][0]
eleNum = len(eleName)
print len(d.values) ,"x",len(d.values[0])


sc = None
image =np.zeros((eleNum,eleNum))

#fig, ax = plt.figure()

MaxVal=0.75
for x in range(len(d.values)):
	for y in range(len(d.values[x])):
		value = d.values[x][y]
		if value >= MaxVal:
			value=MaxVal
		image[x][y]=value+1


r=np.arange(0,eleNum)
eleName = ['Ti','V','Cr','Mn','Fe','Co','Zr','Nb','Mo','Ru','Rh','Pd','Hf','Ta','W','Re','Os','Ir','Pt']
inttheta=[0,50,100,150,200,250,10,61,110,210,260,310,20,70,120,170,220,270,320]
theta=[]
for i in range(len(eleName)):
	theta.append(np.pi*2/360*inttheta[i])
#theta=float(inttheta)*2.0*np.pi/360
#theta=r*np.pi*2/(eleNum-1)

theta2=np.pi*2*np.arange(0,1.001,0.01)
for k in theta2 : 
	ZeroL.append(1)
	HalfL.append(1.5)
	MHalfL.append(0.5)
	QuarterL.append(1.25)
	MQuarterL.append(0.75)

for i in range(0,eleNum): 
	rc('grid', color='#316931', linewidth=1, linestyle='--')
#	rc('grid', color='white', linewidth=1, linestyle='--')
#	rc('nogrid')
#	rc('xtick', labelsize=18)
#	rc('ytick', labelsize=18)

# force square figure and square axes looks better for polar, IMO
#	fig = figure()
	fig = figure(figsize=(8, 8))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar', facecolor='#d5de9c')

#	ax.plot(theta,image[i], color='#ee8d18', marker='o',lw=1, label='Time Saving Curve')
#	ax.plot(theta,image[i], color='green', marker='*',lw=1, label='Time Saving Curve')

	plt.scatter(theta,image[i],s=10, color='black', marker='*',lw=3, label='Execution Time')

	for k in range(0,eleNum): ax.annotate(eleName[k], xy=(theta[k],image[i][k]),size=15)
#	ax.annotate(eleName[i], xy=(np.pi*1.25,0.05),size=15)

#	for k in range(0,eleNum): ax1.annotate(eleName[k], xy=(theta[k],image[i][k], xycoords='figure fraction', xytext=(20, 20), textcoords='offset points', ha="left", va="bottom", bbox=bbox_args, arrowprops=arrow_args)

	ax.plot(theta2,MHalfL, color='green', lw=1, label='Half Time Saved',alpha=transparantVal)
	ax.plot(theta2,MQuarterL, color='blue', lw=1, label='Quarter Time Saved',alpha=transparantVal)
	ax.plot(theta2,ZeroL, color='red', lw=1, label='Bound Line(No Time Saving)',alpha=transparantVal)
	ax.plot(theta2,QuarterL, color='yellow', lw=1, label='Quarter More Time Used',alpha=transparantVal)
	ax.plot(theta2,HalfL, color='magenta', lw=1, label='Half More Time Used',alpha=transparantVal)
	ax.set_title("Others Share Output Files with "+eleName[i], weight='bold', size='larger', position=(0.5, 1.05), horizontalalignment='center', verticalalignment='center',alpha=transparantVal)

#	ax.set_title(eleName[i]+ " Shares Output Files with Others",  position=(0.5, 1.07), horizontalalignment='center', verticalalignment='center')
	ax.legend(loc='upper right', bbox_to_anchor=(0.29,0.14))
#	ax.legend(loc='best')

#	ax.grid(False)
	ax.set_xticks(theta)
#	ax.set_xticks([])
#	ax.set_xticklabels(eleName)
#	ax.set_yticks([])
	ax.set_yticks([0,0.5,0.75,1,1.25,1.5,1.75])
	ax.set_yticklabels([' ',' ',' ',' ',' ',' ',' '])
#	ax.set_yticklabels([eleName[i],'-H','-Q','Z','+Q','+H',' '])
#	ax.set_yticklabels([])

	plt.savefig(fn[0:-4]+'_Radar_'+eleName[i]+"FromOthers.eps")
	plt.savefig(fn[0:-4]+'_Radar_'+eleName[i]+"FromOthers.png",ppi=600)
	plt.close()

	coldata= []
	for k in range(0,eleNum) : coldata.append(image[k][i])
	fig = figure(figsize=(8, 8))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar', facecolor='#d5de9c')


#	ax.plot(theta,coldata, color='green', marker='o',lw=1, label='Time Saving Curve')
	plt.scatter(theta,coldata,s=10, color='black', marker='o',lw=3, label='Execution Time')
	for k in range(0,eleNum): ax.annotate(eleName[k], xy=(theta[k],coldata[k]),size=15)
#	ax.annotate(eleName[i], xy=(np.pi*1.25,0.05),size=15)

	ax.plot(theta2,MHalfL, color='green', lw=1, label='Half Time Saved',alpha=transparantVal)
	ax.plot(theta2,MQuarterL, color='blue', lw=1, label='Quarter Time Saved',alpha=transparantVal)
	ax.plot(theta2,ZeroL, color='red', lw=1, label='Bound Line(No Time Saving)',alpha=transparantVal)
	ax.plot(theta2,QuarterL, color='yellow', lw=1, label='Quarter More Time Used',alpha=transparantVal)
	ax.plot(theta2,HalfL, color='magenta', lw=1, label='Half More Time Used',alpha=transparantVal)
	#ax.plot(theta2,cir, color='red', lw=4, label='Bound Line')
	ax.set_title(eleName[i]+ " Shares Output Files with Others", weight='bold', size='large', position=(0.5, 1.05), horizontalalignment='center', verticalalignment='center',alpha=transparantVal)
#	ax.legend(loc='upper right')
	ax.legend(loc='upper right', bbox_to_anchor=(0.29,0.14))
#	ax.legend(loc='best')

#	ax.grid(False)
#	ax.set_xticks([])
#	ax.set_yticks([])
	ax.set_xticks(theta)
	ax.set_yticks([0,0.5,0.75,1,1.25,1.5,1.75])
	ax.set_yticklabels([' ',' ',' ',' ',' ',' ',' '])
#	ax.set_xticklabels(eleName)
#	ax.set_yticklabels([eleName[i],'-H','-Q','Z','+Q','+H',' '])
#	ax.set_yticklabels([])

	plt.savefig(fn[0:-4]+'_Radar_'+eleName[i]+"ToOthers.eps")
	plt.savefig(fn[0:-4]+'_Radar_'+eleName[i]+"ToOthers.png",ppi=600)
	plt.close()
