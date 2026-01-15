import matplotlib.pyplot as plt
import datetime as DT
#import scipy as sp
import numpy as np
import matplotlib.patches as patches
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import matplotlib
from Flare import *


import sys
sys.path.append('/home/pesce/work/Solar/solarflares/scripts/')

import MET2date as M2D
import Date2MET as D2M

SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30

figsize=(15, 8)

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title




fig1 = plt.figure(figsize=(25,10),facecolor='w')
ax1 = fig1.add_subplot(111)


def parse_SunMon_file():
    
    SunMonFile = open('SUN-3HR.dat')

    LATDectionlist = []

    List = []

    for line in SunMonFile:
        if '#' in line: continue
        line = line.split()
    
        if '#GCNNAME' not in line:
            met  = float(line[3].strip(','))
            ts  = float(line[5].strip(','))
    #met = line[2].strip(',')
    #ts  = float(line[4].strip(','))
    
        if ts>50:
            #date,fff =M2D.computeDate(met)
            #numdate = mdates.date2num(date)
            flare = Flare(float(met), ts)
            List.append(flare)
            print(M2D.computeDate(float(met))[0], ts)

    for i,entry in enumerate(List[:-1]):
        otherentry = List[i+1]
 
        if (float(otherentry.MET) - float(entry.MET)) <= 2*10800.:
    
        
            date,fff =M2D.computeDate(entry.MET)
            numdate = mdates.date2num(date)
            LATDectionlist.append(numdate)
    

    LATDectionarray = np.array(LATDectionlist)           

#This is a list from the catalog and the events from the 25th solar cycle, scanned by hand
detection_list = ['2011-03-07 20:10:40','2011-06-02 09:41:55','2011-06-07 07:33:50', '2011-08-04 04:55:28',\
                '2011-09-06 22:11:50','2011-09-07 23:35:04','2012-01-23 04:06:19', '2012-01-27 19:37:57', \
                '2012-03-05 04:07:30','2012-03-07 00:40:41', '2012-03-09 05:12:07','2012-03-10 21:00:07', \
                '2012-05-17 02:12:24', '2012-06-03 17:38:11', '2012-07-06 23:17:02', '2012-10-23 04:13:59', \
                '2012-11-13 01:34:40', '2012-11-27 15:48:20', '2013-04-11 07:00:01', '2013-05-13 04:31:16', \
                '2013-05-13 17:15:05', '2013-05-14 01:07:57', '2013-05-15 04:12:16', '2013-10-11 06:31:39', \
                '2013-10-25 08:15:52', '2013-10-28 15:32:31', '2014-01-06 07:24:55', '2014-01-07 18:41:01', \
                '2014-02-25 01:09:31', '2014-06-10 14:00:43', '2014-09-01 11:02:03', '2014-09-10 17:35:17', \
                '2015-06-21 05:19:46', '2015-06-25 09:24:19', '2017-09-06 11:46:04','2017-09-07 00:36:17',\
                '2017-09-10 15:52:57', '2021-07-17 03:00:00', '2021-09-17 03:00:00', '2021-10-28 15:00:00', \
                '2022-09-29 09:00:00', '2022-01-20 03:00:00', '2022-10-02 19:30:00', '2023-12-31 22:30:00', \
                '2024-02-09 13:30:00', '2024-02-14 04:30:00', '2024-02-16 06:55:00', '2024-03-10 13:30:00', \
                '2024-07-16 13:30:00', '2024-09-09 07:30:00', '2024-09-14 16:30:00', '2024-10-01 22:30:00', \
                '2024-10-09 01:30:00', '2024-12-08 10:30:00', '2025-03-28 16:30:00', '2025-04-21 22:30:00',\
                '2025-05-31 01:30:00', '2025-07-15 07:30:00','2025-11-11 10:30:00'    ]

#Sun monitor reports this flare '2022-05-29 20:07:00', but from a more careful cross check it does not seem to be a detection of a flare.
#Sun monitor report this flare 2022-08-29 22:30 but again, it does not look like a detection.
#Sun monitor 2024-05-20 07:30 also does not seem to be a detection.
#Sun monitor 2024-08-28 16:30 also does not seem to be a detection

def parse_list():
    flare_detection_list = []
    for flare in detection_list:
        l = flare.split()
        flare_name = '%sUT%s'%(l[0],l[1])
        met_flare_time = D2M.DateString2MET(flare_name)
        date,fff =M2D.computeDate(met_flare_time)
        numdate = mdates.date2num(date)
        flare_detection_list.append(numdate)
    return flare_detection_list

flare_detection_list = parse_list()

LATDectionarray = np.array(flare_detection_list)           

print('**** Total number of SOURCE class flares', len(LATDectionarray))

LLEFlares = [DT.datetime(2025,11,14,8,22,0,0),\
            DT.datetime(2024,10,9,15,43,54,0),DT.datetime(2024,8,1,4,39,0,0),\
            DT.datetime(2024,5,29,18,37,0,0),DT.datetime(2024,5,29,18,27,0,0),\
            DT.datetime(2024,3,10,12,8,0,0),DT.datetime(2024,2,16,7,0,0,0),\
            DT.datetime(2022,9,23,11,32,22,0),DT.datetime(2021,7,3,14,26,0,0),\
            DT.datetime(2013,10,28,20,0,0,0),DT.datetime(2013,10,28,4,0,0,0),\
            DT.datetime(2013,10,25,20,0,0,0),DT.datetime(2012,10,23,3,0,0,0),\
            DT.datetime(2014,2,25,0,0,0,0),DT.datetime(2011,9,24,9,0,0,0),\
            DT.datetime(2011,9,6,22,0,0,0), DT.datetime(2011,8,9,8,0,0,0),\
            DT.datetime(2012,8,6,8,0,0,0),DT.datetime(2010,6,12,0,0,0,0)]

LLEflarelist = []

for flaretime in LLEFlares:
    llenumdate = mdates.date2num(flaretime)
    LLEflarelist.append(llenumdate)

LLEflareArray = np.array(LLEflarelist)
print('**** Total number of LLE flares', len(LLEflareArray))

#The file was downloaded from http://www.sidc.be/silso/datafiles#total
SNfile = open('SN_m_tot_V2.0.txt')

timelist = []
sunspotlist = []

for line in SNfile:
    
    line= line.split()
    
    year = line[0]
    if float(year)>1978:
        month = line[1]
        numspots = float(line[3])
        time = DT.datetime(int(year),int(month),1,0,0,0)
        timelist.append(time)
        sunspotlist.append(numspots)

timearray = np.array(timelist)
spotarray = np.array(sunspotlist)

datemask = timearray>=DT.datetime(1979, 1, 1, 0, 0, 0)
timearray = mdates.date2num(timearray[datemask])
spotarray = spotarray[datemask]

plotstart =  DT.datetime(1979,1,1,0,0,0)
#plotend =  DT.datetime(2015,10,1,0,0,0)
#plotend =  DT.datetime(2017,12,1,0,0,0)
plotend =  DT.datetime(2026,1,15,0,0,0)

START = mdates.date2num(plotstart)
END = mdates.date2num(plotend)


GRSstartTime = DT.datetime(1980,1,1,0,0,0)
GRSendTime = DT.datetime(1989,1,1,0,0,0)
# convert to matplotlib date representation
GRSstart = mdates.date2num(GRSstartTime)
GRSend = mdates.date2num(GRSendTime)
GRSwidth = GRSend - GRSstart

grstimes = [DT.datetime(1982,6,3,1,0,0,0),DT.datetime(1984,4,25,1,0,0,0),DT.datetime(1988,12,16,1,0,0,0),DT.datetime(1989,3,6,1,0,0,0)]

GRSflarelist = []
for flaretime in grstimes:
    grsnumdate = mdates.date2num(flaretime)
    GRSflarelist.append(grsnumdate)

GRSarray = np.array(GRSflarelist)

plt.hist(GRSarray,20,histtype='stepfilled',color='green',alpha=0.5,label='SMM-GRS')


GRANATstartTime = DT.datetime(1990,1,1,0,0,0)
GRANATendTime = DT.datetime(1994,1,1,0,0,0)
# convert to matplotlib date representation
GRANATstart = mdates.date2num(GRANATstartTime)
GRANATend = mdates.date2num(GRANATendTime)
GRANATwidth = GRANATend - GRANATstart

granattimes = [DT.datetime(1990,5,11,20,0,0,0),DT.datetime(1990,6,11,9,0,0,0),DT.datetime(1991,3,12,12,0,0,0),DT.datetime(1991,3,22,22,0,0,0),DT.datetime(1991,3,31,19,0,0,0),DT.datetime(1992,2,11,4,0,0,0)]

GRANATflarelist = []
for flaretime in granattimes:
    granatnumdate = mdates.date2num(flaretime)
    GRANATflarelist.append(granatnumdate)

GRANATarray = np.array(GRANATflarelist)

# Plot rectangle
#GRANATrect = Rectangle((GRANATstart, 0), GRANATwidth, 7, color='red',alpha=0.5,linewidth=3)
#ax1.add_patch(GRANATrect)
#ax1.text(DT.datetime(1990,4,1,0,0,0), 5, 'GRANAT', size=20, ha='left', va='center')

plt.hist(GRANATarray,7,histtype='stepfilled',color='yellow',alpha=0.75,label='GRANAT-PHEBUS')


################GAMMA-1#####################
gamma1flaretimes = np.array([mdates.date2num(DT.datetime(1991,3,26,1,0,0)),mdates.date2num(DT.datetime(1991,6,15,1,0,0))])

GAMMA1startTime = DT.datetime(1990,7,1,0,0,0)
GAMMA1endTime = DT.datetime(1992,7,1,0,0,0)
# convert to matplotlib date representation
GAMMA1start = mdates.date2num(GAMMA1startTime)
GAMMA1end = mdates.date2num(GAMMA1endTime)

gamma1times = np.array([mdates.date2num(DT.datetime(1991,3,26,1,0,0,0)),mdates.date2num(DT.datetime(1991,6,15,1,0,0,0))])

plt.hist(gamma1flaretimes,1,histtype='stepfilled',color='magenta',alpha=0.5,label='GAMMA-1')



EGRETstartTime = DT.datetime(1990,1,1,0,0,0)
EGRETendTime = DT.datetime(1999,1,1,0,0,0)
# convert to matplotlib date representation
EGRETstart = mdates.date2num(EGRETstartTime)
EGRETend = mdates.date2num(EGRETendTime)
EGRETwidth = EGRETend - EGRETstart

egretmissiontime = np.array([mdates.date2num(EGRETstartTime)],) 

egrettimes = [DT.datetime(1991,6,4,3,0,0,0),DT.datetime(1991,6,6,1,0,0,0),DT.datetime(1991,6,9,1,0,0,0),DT.datetime(1991,6,11,2,0,0,0)]
EGRETflarelist = []

for flaretime in egrettimes:
    egretnumdate = mdates.date2num(flaretime)
    EGRETflarelist.append(egretnumdate)


EGRETarray = np.array(EGRETflarelist)
#plt.hist(EGRETarray,4,histtype='stepfilled',color='blue',alpha=0.95,label='CGRO-EGRET')
plt.hist(EGRETarray,3,histtype='stepfilled',color='blue',label='CGRO-EGRET')

# Plot rectangle
#EGRETrect = Rectangle((EGRETstart, 0), EGRETwidth, 4, color='orange',alpha=0.5,linewidth=3)
#egretflares = sp.array([DT.datetime(1991,06,11,0,0,0),DT.datetime(1991,06,30,0,0,0),DT.datetime(1991,9,30,0,0,0)])


coronasflares = [DT.datetime(2001,8,25,0,0,0),DT.datetime(2003,10,28,0,0,0),DT.datetime(2003,11,4,0,0,0),DT.datetime(2005,1,20,0,0,0)]

CORONASflarelist = []

for flaretime in coronasflares:
    coronanumdate = mdates.date2num(flaretime)
    CORONASflarelist.append(coronanumdate)

CORONASarray = np.array(CORONASflarelist)

plt.hist(CORONASarray,10,histtype='stepfilled',color='green',alpha=0.75,label='SONG-CORONAS')
    
#ax1.add_patch(EGRETrect)
#ax1.text(DT.datetime(1992,8,1,0,0,0), 2, 'EGRET', size=20, ha='left', va='center')

LATstartTime = DT.datetime(2006,6,1,0,0,0)

#LATendTime = DT.datetime(2017,12,1,0,0,0)
LATendTime = DT.datetime(2026,1,15,0,0,0)
# convert to matplotlib date representation
LATstart = mdates.date2num(LATstartTime)
LATend = mdates.date2num(LATendTime)
LATwidth = LATend - LATstart

total_lat_flares = np.concatenate((LATDectionarray, LLEflareArray)) 

plt.hist(total_lat_flares,20,histtype='stepfilled',color='red',alpha=0.5,label='Fermi-LAT')

print('**** Total number of LAT flares', len(total_lat_flares))

#ax1.text(DT.datetime(2010,8,1,0,0,0), 28, 'Fermi-LAT', size=25, ha='left', va='center',rotation=90)
#plt.legend(bbox_to_anchor=(0.9, 0.97),frameon=0)
plt.legend(bbox_to_anchor=(0.74, 0.99),frameon=0)
ax12 = ax1.twinx()
ax12.set_ylim(0,370)

ax12.plot(timearray,spotarray,marker='o',ls='--')
ax12.set_ylabel('Monthly average Sunspot number',fontsize=25)
# assign date locator / formatter to the x-axis to get proper labels
locator = mdates.AutoDateLocator(minticks=3)
formatter = mdates.AutoDateFormatter(locator)

ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_major_formatter(formatter)

plt.xlim([START,END])
ax1.set_ylim([0, 28])
ax1.set_ylabel('Number of > 25 MeV Solar flares',fontsize=25)
ax1.set_xlabel('Year',fontsize=25)

#Include the times of the behind-the-limb solar flares
btl_height = 20
lebtl_color = 'black'
ax1.plot(np.array([DT.datetime(1989,9,29,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color=lebtl_color, alpha=0.5)

#P.arrow( x, y, dx, dy, **kwargs )
#ax1.arrow(DT.datetime(1989,9,29,0,0,0), 20, 0.0, -10, head_width=125, head_length=1, color='r')

ax1.plot(np.array([DT.datetime(1991,5,1,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color=lebtl_color,alpha=0.5)

#ax1.arrow(DT.datetime(1991,6,1,0,0,0), 20, 0.0, -10, head_width=125, head_length=1, color='r')

ax1.plot(np.array([DT.datetime(1991,6,30,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color=lebtl_color,alpha=0.5)

#ax1.arrow(DT.datetime(1991,6,30,0,0,0), 20, 0.0, -10, head_width=125, head_length=1, color='r')

####LAT BTL flares
ax1.plot(np.array([DT.datetime(2013,10,11,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2014,1,6,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2014,9,1,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2021,7,17,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2021,9,17,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2022,9,29,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')

ax1.plot(np.array([DT.datetime(2024,2,14,0,0,0)]),np.array([btl_height]),marker='*',markersize=25,color='red')
#######

ax1.text(DT.datetime(1980,2,1,0,0,0), 27, 'Behind-the-limb flares',color='black',size=25, ha='left', va='center')
ax1.text(DT.datetime(1980,2,1,0,0,0), 25.5, '$\star$  <100 MeV',color=lebtl_color,alpha=0.5,size=25, ha='left', va='center')
ax1.text(DT.datetime(1980,2,1,0,0,0), 24., '$\star$  >100 MeV',color='red',size=25, ha='left', va='center')


plt.show()
