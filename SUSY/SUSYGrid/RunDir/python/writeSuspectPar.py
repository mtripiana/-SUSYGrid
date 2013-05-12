#!/usr/local/bin/python

import os
import sys
import string, re, random, math


#arguments: M1, M3, mu, At
M1 = sys.argv[1]
M3 = sys.argv[2]
mu = sys.argv[3]
Msq = sys.argv[4]
At = sys.argv[5]
tanBeta = sys.argv[6]
Msf12 = 2.5E+03
Msf3 = 2.5E+03

# inputs remaining constant through the scan:
SLHAInputTemplate = string.Template("""\
Block MODSEL                 # Select model
   1    ${MODSEL}            # general MSSM low scale
Block SU_ALGO  # !Optional SUSPECT v>=2.3* block: algorithm control parameters
# !IF block absent (or if any parameter undefined), defaut values are taken
   2    21  # 2-loop RGE (defaut, 1-loop RGE is: 11 instead)
   3    1   # 1: g_1(gut) = g_2(gut) consistently calculated from input
#   (other possibility is 0: High scale input =HIGH in block EXTPAR below)
   4    2   # RGE accuracy: 1: moderate, 2: accurate (but slower)
   6    1   #  1: M_Hu, M_Hd input (default in constrained models)
#        (other possibility 0: MA_pole, MU(EWSB) input instead)
   7    1   #  choice for sparticles masses rad. corr. (=/= h):
#               2 ->all (recommended, defaut); 1->no R.C. in squarks & gauginos.
   8    0   # 1 (default): EWSB scale=(mt_L*mt_R)^(1/2)
#         (Or = 0: arbitrary EWSB scale: give EWSB in Block EXTPAR below)
   9    2   # Final spectrum accuracy: 1 -> 1% acc.; 2 -> 0.01 % acc.(defaut)
   10   2   # Higgs boson masses rad. corr. calculation options:
#             A simple (but very good) approximation (advantage=fast)  : 0
#             Full one-loop calculation                                : 1
#             One-loop  + dominant DSVZ 2-loop (defaut,recommended)    : 2
   11   0   # Higher order Higgs 'scheme' choice in rad. corr. at mZ:
#          RUNNING DRbar Higgs masses at loop-level at mZ (defaut)    : 0
#          POLE          Higgs masses at loop-level at mZ             : 1
Block SMINPUTS               # Standard Model inputs
   1     1.27932904E+02  # alpha_em^-1(MZ)^MSbar
#   2     1.16639000E-05  # G_mu [GeV^-2]
   3     1.17200000E-01  # alpha_s(MZ)^MSbar
#   4     9.11876000E+01  # m_Z(pole)
   5     4.25000000E+00  # m_b(m_b), MSbar
   6     1.72900000E+02  # m_t(pole)
   7     1.77700000E+00  # m_tau(pole)                   
Block MINPAR                 # Input parameters
#   input for GMSB models (! comment (#) all other (mSUGRA,AMSB) lines):
Block EXTPAR                 # Input parameters
   0     9.11876000E+01   # EWSB_scale
   1     ${M1}      # M_1
   2     2.5E+03    # M_2
   3     ${M3}      # M_3
   11    ${At}      # A_t
   12    0.00E+00   # A_b
   13    0.00E+00   # A_tau
   14    0.00E+00   # A_u
   15    0.00E+00   # A_d
   16    0.00E+00   # A_e
   23    ${mu}      # mu(EWSB)
   26    2.00E+03   # MA_pole
   25    ${tanBeta} # tanbeta(MZ)
   31    ${Msf12}   # M_eL
   32    ${Msf12}   # M_muL
   33    ${Msf3}    # M_tauL
   34    ${Msf12}   # M_eR
   35    ${Msf12}   # M_muR
   36    ${Msf3}    # M_tauR
   41    ${Msq}     # M_q1L
   42    ${Msq}     # M_q2L
   43    ${Msq}     # M_q3L
   44    ${Msf12}   # M_uR
   45    ${Msf12}   # M_cR
   46    ${Msf3}    # M_tR
   47    ${Msq}     # M_dR
   48    ${Msq}     # M_sR
   49    ${Msq}     # M_bR
""")


################################################################################
SLHAInput = SLHAInputTemplate.substitute({
    'MODSEL' : 0,
    'M1' : M1,
    'M3' : M3,
    'mu' : mu,
    'Msq': Msq,
    'At' : At,
    'Msf12' : Msf12,
    'Msf3' : Msf3,
    'tanBeta' : tanBeta,
    })
################################################################################
InFile = open('../SuSpect/suspect2_lha.in', 'w')
InFile.write(SLHAInput)
InFile.close()
