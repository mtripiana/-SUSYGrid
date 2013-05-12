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

GRIDtype=sys.argv[2]  #0=gl_neut, 1=sq_neut

Hmass=sys.argv[3]  #positive value to change Higgs mass!

M1min = 800
M1max = 950
M1step = 25 

mumin = 100
mumax = 1600
mustep = 25 

M1mumin = 0.8
M1mumax = 1.2

M3min = 800
M3max = 1500
M3step = 50 

Msqmin = 800
Msqmax = 1500
Msqstep = 50 

v_At = [0] #At possible values
    
doGmassScan=False  # Gravitino mass scan
minGmass=1E-10
maxGmass=1E-06
GmassPoints=1
stepGmass=(maxGmass-minGmass)/GmassPoints

useM1muRelation=False
useMuPositive=True

vbos=False

#open config file
fo = open(CFILE, "wb")

################################################################################

# SUSY-HIT: generate SLHA files one by one
Progress = 0

#compute running points

iN_m1 = (M1max - M1min)/M1step
iN_m3 = (M3max - M3min)/M3step
iN_mu = (mumax - mumin)/mustep
iN_msq = (Msqmax - Msqmin)/Msqstep

if GRIDtype == "0":
    iN_msq = 1
    Msqmin = 2.5E+03
    print "GRID gl_neut RUNNING NOW!!"
else:
    iN_m3 = 1
    M3min = 2.5E+03


for ir_m1 in range(0,iN_m1):
    m1v = M1min + ir_m1 * M1step

#    print 'M1',m1v

    for ir_mu in range(0,iN_mu):

        if useM1muRelation==True:
            muv = (m1v / random.uniform(M1mumin, M1mumax)) * ((-1) ** random.randint(0,1))
        else:
            muv = mumin + ir_mu * mustep
            
        if useMuPositive==True:
            muv = math.fabs(muv)
            
#        print 'mu',muv
            
        for ir_m3 in range(0,iN_m3):
            
            m3v = M3min + ir_m3 * M3step

            #make sure that the (aprox) M(chi10) is greater than M(gluino)
            if m1v >= m3v:
                continue

#            print 'M3',m3v
            
            for ir_msq in range(0, iN_msq):

                msqv = Msqmin + ir_msq * Msqstep
                    
                #make sure that the (aprox) M(chi10) is greater than M(gluino)
                if m1v >= msqv:
                    continue

#                print 'msq',msqv
                
                for atv in v_At:

                    iGmv = 0
                    for iGmv in range(0, GmassPoints): 
                
                        iGmv += 1
                        Progress += 1
                            
                        if doGmassScan==True:
                            Gmass = minGmass + iGmv*stepGmass
                        else:
                            Gmass = -999
                                        
                        if (Progress % ReportProgressOnceEvery_SLHAs == 0):
                            print 'SUSY-HIT',Progress,'points'# through',GmassNumPoints

                        print str(m1v),'   ',str(m3v),'  ',str(muv),'  ',str(msqv),'  ',str(atv),'  ',str(Gmass),'  ',str(iGmv),'  ',str(GRIDtype)

                        fo.write(str(m1v)+'   '+str(muv)+'  '+str(m3v)+'  '+str(msqv)+'  '+str(atv)+'  '+str(Gmass)+'  '+str(iGmv)+'  '+str(GRIDtype)+'  '+str(Hmass)+' \n');

#end of loops

# Close config file
fo.close()


