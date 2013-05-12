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

#gluino_neutralino grid 

muToM1 = 0.99

minMu = 150
maxMu = 750 #below M3!
npointsMu = 300
stepMu = (maxMu-minMu)/npointsMu

minGmass=1E-9
maxGmass=1E-06
npointsGmass=600
stepGmass=(maxGmass-minGmass)/npointsGmass

if GRIDtype=='0':
    v_M3  = [800]#,850,900,950,1000,1050,1100,1150,1200,1250,1300]#,1350,1400]
    v_Msq = [2500]
else:
    v_M3  = [2500]
    v_Msq = [800]#,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400]

At = 0

#Hmass = 125.
#tanBeta = 1.5

vbos=False

#open config file
fo = open(CFILE, "wb")

################################################################################

# SUSY-HIT: generate SLHA files one by one
Progress = 0

for nmu in range(npointsMu):
    for ngm in range(npointsGmass):

        Progress += 1

        mu = minMu + nmu*stepMu
        M1 = mu*muToM1
                
        M3 = v_M3[0]
        Msq = v_Msq[0]

        if mu > M3:
            continue

        if mu > Msq:
            continue
        
        Gmass = minGmass + ngm*stepGmass
        
        if (Progress % ReportProgressOnceEvery_SLHAs == 0):
            print 'SUSY-HIT',Progress,'points'# through',GmassNumPoints
                
        fo.write(str(M1)+'   '+str(mu)+'  '+str(M3)+'  '+str(Msq)+'  '+str(At)+'  '+str(Gmass)+'  '+str(ngm)+'  '+str(GRIDtype)+'  '+str(Hmass)+'  '+str(tanBeta)+' \n');

#end of loops

# Close config file
fo.close()


