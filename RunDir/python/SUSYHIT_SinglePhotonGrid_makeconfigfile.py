#! /usr/bin/python
#
import os, sys, commands
import posix
import getopt, string
import re, random, math
import posix
import time
from stat import *
from glob import glob

if len(sys.argv) < 2:  # the program name and one argument
    # stop the program and print an error message
    sys.exit("Must provide output file name!")
        
############################################################################################
### COMMON PARAMETER  ######

# scan inputs:
ReportProgressOnceEvery_SLHAs = 1000
#NumPoints = 10000

CFILE=sys.argv[1]

GRIDtype=str(sys.argv[2])  #0=gl_neut, 1=sq_neut

Hmass=sys.argv[3]  #positive value to change Higgs mass!

tanBeta=sys.argv[4]  #tanBeta value


if GRIDtype=='0':
    #* >>> gluino_neutralino grid 

    #v_M1 = [200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
    #v_mu = [140,200,270,330,385,440,492,540,595,647,698,749,800,850,902,953,1004,1055,1105,1156,1207,1258,1310,1363,1414,1465,1520]

    #v_M1 = [600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400]
    #v_mu = [590,647,698,749,800,850,902,953,1004,1055,1105,1156,1207,1258,1310,1361,1412]

    #new setup as function of (regular) mu  [04-04-2013]   BR(chi10 -> Ggamma)~50%
    v_M1 = [600,647,697,745,795,845,893,942,990,1040,1090,1140,1190,1238,1288]#,1338,1388]
    v_mu = [600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300]#,1350,1400]

    v_M3  = [800,850,900,950,1000,1050,1100,1150,1200,1250,1300]#,1350,1400]
    v_Msq = [2500]

elif GRIDtype=='1':
    #* >>> sq_neutralino grid 

    #new setup as function of (regular) mu  [04-04-2013]   BR(chi10 -> Ggamma)~50%
    v_M1 = [600,647,697,745,795,845,893,942,990,1040,1090,1140,1190,1238,1288]#,1338,1388]
    v_mu = [600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300]#,1350,1400]

    v_M3  = [2500]
    v_Msq = [800,850,900,950,1000,1050,1100,1150,1200,1250,1300]

elif GRIDtype=='2':
    #* >>> EWK neutralino grid 

    #new setup as function of (regular) mu  [04-04-2013]   BR(chi10 -> Ggamma)~50%
    v_M1 = [157,180,205,54,352,451,549,647,745,845,942,1040,1140,1238]
    v_mu = [150,175,200,250,350,450,550,650,750,850,950,1050,1150,1250]

    v_M3  = [2500]
    v_Msq = [2500]
else:
    sys.exit(0)

Minmu=400 # min f , mu = M1/f
Maxmu=1300 # max f , mu = M1/f

MinM1=400 # min f , mu = M1/f
MaxM1=1300 # max f , mu = M1/f

MinM1mu=0.98 # min f , mu = M1/f
MaxM1mu=1.0 # max f , mu = M1/f

v_At = [0] #At possible values

doGmassScan=False  # Gravitino mass scan
minGmass=1E-10
maxGmass=1E-06
GmassPoints=1
stepGmass=(maxGmass-minGmass)/GmassPoints

useM1muRelation=False
useFixedMu=True
useMuPositive=True

vbos=False


#open config file
fo = open(CFILE, "wb")

################################################################################

# SUSY-HIT: generate SLHA files one by one
Progress = 0

for atv in v_At:
    for imu in range(len(v_mu)):
        for m3v in v_M3:
            for msqv in v_Msq:
                iGmv = 0
                while iGmv < GmassPoints: 
                
                    iGmv += 1
                    Progress += 1
                
                    M1 = v_M1[imu]
                
                    M3 = m3v

                    Msq = msqv

                    mu = v_mu[imu]
                    #make sure that the (aprox) M(chi10) is greater than M(gluino)
#                    if M1 >= M3:
                    if mu > M3:
                        continue
#                    if M1 >= Msq:
                    if mu > Msq:
                        continue

                    if useM1muRelation==True:
                        M1 = (mu * random.uniform(MinM1mu, MaxM1mu)) * ((-1) ** random.randint(0,1))
                    elif useFixedMu==True:
                        M1 = v_M1[imu]
                    else:
                        M1 = random.randint(MinM1, MaxM1) * ((-1) ** random.randint(0,1))

                    if useMuPositive==True:
                        mu = math.fabs(mu)
                            
                    At = atv
                            
                    if doGmassScan==True:
                        Gmass = minGmass + iGmv*stepGmass
                    else:
                        Gmass = -999

                    if (Progress % ReportProgressOnceEvery_SLHAs == 0):
                        print 'SUSY-HIT',Progress,'points'# through',GmassNumPoints

                    fo.write(str(M1)+'   '+str(mu)+'  '+str(M3)+'  '+str(Msq)+'  '+str(At)+'  '+str(Gmass)+'  '+str(iGmv)+'  '+str(GRIDtype)+'  '+str(Hmass)+'  '+str(tanBeta)+' \n');

#end of loops

# Close config file
fo.close()


