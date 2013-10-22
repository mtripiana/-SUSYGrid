#!/usr/bin/env python                                                                                                                                                                                          
import sys, os, argparse
from array import array
from ROOT import *

def SetLegendStyle(leg, fcolor=0, bsize=0, fstyle=1001):
        leg.SetFillColor(fcolor)
        leg.SetFillStyle(fstyle)
        leg.SetBorderSize(bsize)

def SetMyPalette(name="palette", ncontours=999):
    """Set a color palette from a given RGB list                                
    stops, red, green and blue should all be lists of the same length           
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
        # elif name == "whatever":                                              
        # (define more palettes)                                                
    else:
        # default palette, looks cool                                           
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.65] #0.51-->0.65                     
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.80, 1.00, 0.12, 0.00, 0.00] # 0.51--->0.8                    
        ncontours=100

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)

    # For older ROOT versions                                                   
    #gStyle.CreateGradientColorTable(npoints, s, r, g, b, ncontours)            
    gStyle.SetNumberContours(ncontours)

def SetStyle():                      
                                     
    ##  gStyle.SetPalette(1)         
    SetMyPalette()                   
    gStyle.SetFrameFillColor(0)      
    gStyle.SetFrameBorderSize(0)     
    gStyle.SetFrameBorderMode(0)     
    ##  gStyle.SetFillColor(0)       
    gStyle.SetCanvasColor(0)         
    gStyle.SetOptStat(0)             
    gStyle.SetTitleBorderSize(0)     
    gStyle.SetTitleFillColor(0)      
    gStyle.SetTextFont(42)           
    gStyle.SetLabelFont(42,"XY")     
    gStyle.SetTitleFont(42,"XY")     
    gStyle.SetEndErrorSize(0)      

def getMGL(m3):
	p0=166.071
	p1=0.89076
	return p0+p1*m3

def getMNT(mu):
	p0=-29.3908
	p1=1.01192
	return p0+p1*mu

def getM3(mgl):
	p0=166.071
	p1=0.89076
	return (mgl-p0)/p1

def getMu(mnt):
	p0=-29.3908
	p1=1.01192
	return (mnt-p0)/p1

if __name__ == '__main__':

    # config
    parser = argparse.ArgumentParser(description='draw particles decays from grid slha files')
    parser.add_argument('--infile', dest='infile', action='store', help='File with the list of slha files to consider.', default='slhafiles.txt')
    parser.add_argument('--fullbr', action='store_true', help='Do full (sgl ...> n1) br calculation', default=False)
    parser.add_argument('--fpath', dest='fpath', action='store', help='Path to slha files to be read.', default="/Users/tripiana/MyWork/CERN2013/SUSY/PhotonMET/SPgrid/SPgrid_photonX_request_Jul13/slha/")
    parser.add_argument('--outpath', dest='outpath', action='store', help='Path to save output plots.', default="../plots/decays/")

    config = parser.parse_args()
    

    #open parameters file
    try:
	    fin =  open(config.infile,'r')
	    lines = fin.readlines()
	    fin.close()                                           
	    
	    files = map(lambda s: s.rstrip('\n'), lines)
    except:                                              
	    print 'File not found! Try again...'             
	    sys.exit(1)                                      
	    
    M3=[]                                                
    mu=[]                                                
    gl_n1g=[]   #  BR(~g -> ~chi_10 g)                                               
    gl_n2g=[]   #  BR(~g -> ~chi_20 g)                                          
    gl_n3g=[]   #  BR(~g -> ~chi_30 g)                                          
    gl_gravg=[] #  BR(~g -> ~G      g)                                        
    
    gl_n1qq=[]  # BR(~g -> ~chi_10 q  qb)
    gl_n2qq=[]  # BR(~g -> ~chi_20 q  qb)
    gl_n3qq=[]  # BR(~g -> ~chi_30 q  qb)
    gl_c1qq=[]  # BR(~g -> ~chi_10 q  qb)
    
    n1_gravgam=[] # BR(~chi_10 -> ~G        gam)  
    n1_gravz=[]   # BR(~chi_10 -> ~G        Z)
    n1_gravh=[]   # BR(~chi_10 -> ~G        h)

    n2_n1=[] # BR(~chi_20 -> ~chi10 ...
    n2_c1=[] # BR(~chi_20 -> ~chi1+ ...
    n3_n1=[] # BR(~chi_30 -> ~chi10 ...
    n3_n2=[] # BR(~chi_30 -> ~chi20 ...
    n3_c1=[] # BR(~chi_30 -> ~chi1+ ...
    c1_n1=[] # BR(~chi_1+ -> ~chi10 ...
    
    for f in files:                                       

	    try:
		    fin =  open(config.fpath+f,'r')
		    lines = fin.readlines()
		    fin.close()                                           
		    
		    rows = map(lambda s: s.rstrip('\n'), lines)
	    except:                                              
		    print 'File ',config.fpath+f,' not found! Skipping...'             
		    continue
	    
	    M3.append(float(f.split('_')[4]))
	    mu.append(float(f.split('_')[-1].split('.')[0]))
	    
		#gluino->...
	    n1g=0
	    n2g=0
	    n3g=0
	    gravg=0
	    gravgam=0
	    gravz=0
	    gravh=0
	    n1qq=0
	    n2qq=0
	    n3qq=0
	    c1qq=0
		
	    #secondary decays to n1
	    n2n1=0
	    n2c1=0
	    n3n1=0
	    n3n2=0
	    n3c1=0
	    c1n1=0	
		
	    for r in rows:
		    if "# BR(" not in r:  #just look at gluino decays for now
			    continue                                     
		    
		    dp = float(r.split()[0])
		    
		    if "BR(~g -> ~G      g)" in r:
			    gravg = dp
			    
		    if "BR(~g -> ~chi_10" in r:
			    if "g)" in r:
				    n1g = dp
			    elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
				    n1qq+=dp
				
		    if "BR(~g -> ~chi_20 " in r:
			    if "g)" in r:
				    n2g = dp
			    elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
				    n2qq+=dp

		    if "BR(~g -> ~chi_30 " in r:
			    if "g)" in r:
				    n3g = dp
			    elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
				    n3qq+=dp

		    if ("BR(~g -> ~chi_1+" in r) or ("BR(~g -> ~chi_1-" in r):
			    c1qq+=dp

		    if "BR(~chi_10 -> ~G        gam)" in r:
			    gravgam = dp

		    if "BR(~chi_10 -> ~G        Z)" in r:
			    gravz = dp

		    if "BR(~chi_10 -> ~G        h)" in r:
			    gravh = dp

		    if "BR(~chi_1+ -> ~chi_10 " in r:
			    #if ("u    db)" in r) or ("c    sb)" in r) or ("e+   nu_e)" in r) or ("mu+  nu_mu)" in r) or ("tau+ nu_tau)" in r): #not needed
			    c1n1 += dp
			
		    if "BR(~chi_20 -> ~chi_10 " in r: 
			    n2n1 += dp
			    
		    if ("BR(~chi_20 -> ~chi_1+ " in r) or ("BR(~chi_20 -> ~chi_1- " in r):
			    n2c1 += dp
				    
		    if "BR(~chi_30 -> ~chi_10 " in r: 
			    n3n1 += dp

		    if "BR(~chi_30 -> ~chi_20 " in r: 
			    n3n2 += dp

		    if ("BR(~chi_30 -> ~chi_1+ " in r) or ("BR(~chi_30 -> ~chi_1- " in r): 
			    n3c1 += dp

				
	    gl_n1g.append(n1g)
	    gl_n2g.append(n2g)
	    gl_n3g.append(n3g)
	    gl_gravg.append(gravg)
	    
	    gl_n1qq.append(n1qq)
	    gl_n2qq.append(n2qq)
	    gl_n3qq.append(n3qq)
	    gl_c1qq.append(c1qq)
	    
	    n1_gravgam.append(gravgam)
	    n1_gravz.append(gravz)
	    n1_gravh.append(gravh)

	    c1_n1.append(gravgam)
	    n2_n1.append(gravgam)
	    n2_c1.append(gravz)
	    n3_n1.append(gravh)
	    n3_n2.append(gravh)
	    n3_c1.append(gravh)
		
	    
    mubins=52
    mumin=100
    mumax=1400
    m3bins=24
    m3min=800
    m3max=1400

    h_gl_n1g = TH2F('h_gl_n1g',';M3 (GeV);#mu (GeV)',m3bins,m3min,m3max,mubins,mumin,mumax)
    h_gl_n1g.GetYaxis().SetTitleSize(0);
    
    h_gl_n2g = h_gl_n1g.Clone("h_gl_n2g")
    h_gl_n3g = h_gl_n1g.Clone("h_gl_n3g")
    h_gl_n1qq = h_gl_n1g.Clone("h_gl_n1qq")
    h_gl_n2qq = h_gl_n1g.Clone("h_gl_n2qq")
    h_gl_n3qq = h_gl_n1g.Clone("h_gl_n3qq")
    h_gl_c1g = h_gl_n1g.Clone("h_gl_c1qq")
    h_gl_gravg = h_gl_n1g.Clone("h_gl_gravg")

    h_gl_n1 = h_gl_n1g.Clone("h_gl_n1")
    h_gl_n2 = h_gl_n1g.Clone("h_gl_n2")
    h_gl_n3 = h_gl_n1g.Clone("h_gl_n3")
    h_gl_c1 = h_gl_n1g.Clone("h_gl_c1")
    
    h_n1_gravgam = h_gl_n1g.Clone("h_n1_gravgam")
    h_n1_gravz = h_gl_n1g.Clone("h_n1_gravz")
    h_n1_gravh = h_gl_n1g.Clone("h_n1_gravh")
    
    mu_axis = TGaxis(m3min,mumin,m3min,mumax,mumin,mumax)
    gl_axis = TGaxis(m3min,mumin-200,m3max,mumin-200,getMGL(m3min),getMGL(m3max))
    nt_axis = TGaxis(m3min-100,mumin,m3min-100,mumax,getMNT(mumin),getMNT(mumax))
    
    gl_axis.SetTitle("gluino mass (GeV)")
    nt_axis.SetTitle("neutralino mass (GeV)")
    mu_axis.SetTitle("#mu (GeV)")
    gl_axis.SetTitleOffset(1.2)
    nt_axis.SetTitleOffset(1.2)
    mu_axis.SetTitleOffset(1.3)
    gl_axis.SetTitleSize(0.035)
    nt_axis.SetTitleSize(0.035)
    mu_axis.SetTitleSize(0.035)
    gl_axis.SetLabelSize(0.035)
    nt_axis.SetLabelSize(0.035)
    mu_axis.SetLabelSize(0.035)
    gl_axis.SetTextFont(42)
    nt_axis.SetTextFont(42)
    mu_axis.SetTextFont(42)
    gl_axis.SetTitleFont(42)
    nt_axis.SetTitleFont(42)
    mu_axis.SetTitleFont(42)
    gl_axis.SetLabelFont(42)
    nt_axis.SetLabelFont(42)
    mu_axis.SetLabelFont(42)
    gl_axis.SetTickSize(0.01)
    nt_axis.SetTickSize(0.01)
    mu_axis.SetTickSize(0.01)
    
    nothere=TGraph(3)
    nothere.SetPoint(1,getM3(800),getMu(800))
    nothere.SetPoint(2,getM3(800),getMu(1400))
    nothere.SetPoint(3,getM3(1400),getMu(1400))
    nothere.SetFillColor(ROOT.kGray)
    nothere.SetFillStyle(3001)
    
    nothere1=TGraph(3)
    nothere1.SetPoint(1,800,800)
    nothere1.SetPoint(2,800,1400)
    nothere1.SetPoint(3,1400,1400)
    nothere1.SetFillColor(ROOT.kGray)
    nothere1.SetFillStyle(3001)
    
    #fill histos
    for i in range(len(M3)):
	    if config.fullbr:
		    h_gl_n1g.Fill(M3[i],mu[i],gl_n1g[i])
		    h_gl_n2g.Fill(M3[i],mu[i],gl_n2g[i] * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
		    h_gl_n3g.Fill(M3[i],mu[i],gl_n3g[i] * ( n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i] ))
		    h_gl_gravg.Fill(M3[i],mu[i],gl_gravg[i])
		    
		    h_gl_n1qq.Fill(M3[i],mu[i],gl_n1qq[i])
		    h_gl_n2qq.Fill(M3[i],mu[i],gl_n2qq[i] * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
		    h_gl_n3qq.Fill(M3[i],mu[i],gl_n3qq[i] * ( n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i] ))
		    h_gl_c1qq.Fill(M3[i],mu[i],gl_c1qq[i] * c1_n1[i])
		    
		    h_gl_n1.Fill(M3[i],mu[i],gl_n1qq[i]+gl_n1g[i])
		    h_gl_n2.Fill(M3[i],mu[i],(gl_n2qq[i]+gl_n2g[i]) * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
		    h_gl_n3.Fill(M3[i],mu[i],(gl_n3qq[i]+gl_n3g[i]) * ( n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i] ))
		    h_gl_c1.Fill(M3[i],mu[i],gl_c1qq[i] * c1_n1[i])
		    
		    
	    else:
		    h_gl_n1g.Fill(M3[i],mu[i],gl_n1g[i])
		    h_gl_n2g.Fill(M3[i],mu[i],gl_n2g[i])
		    h_gl_n3g.Fill(M3[i],mu[i],gl_n3g[i])
		    h_gl_gravg.Fill(M3[i],mu[i],gl_gravg[i])
		    h_gl_n1qq.Fill(M3[i],mu[i],gl_n1qq[i])
		    h_gl_n2qq.Fill(M3[i],mu[i],gl_n2qq[i])
		    h_gl_n3qq.Fill(M3[i],mu[i],gl_n3qq[i])
		    h_gl_c1qq.Fill(M3[i],mu[i],gl_c1qq[i])
		    
		    h_gl_n1.Fill(M3[i],mu[i],gl_n1qq[i]+gl_n1g[i])
		    h_gl_n2.Fill(M3[i],mu[i],gl_n2qq[i]+gl_n2g[i]) 
		    h_gl_n3.Fill(M3[i],mu[i],gl_n3qq[i]+gl_n3g[i]) 
		    h_gl_c1.Fill(M3[i],mu[i],gl_c1qq[i])
		    
	    h_n1_gravgam.Fill(M3[i],mu[i],n1_gravgam[i])
	    h_n1_gravz.Fill(M3[i],mu[i],n1_gravz[i])
	    h_n1_gravh.Fill(M3[i],mu[i],n1_gravh[i])
	    
    #output plots

    SetStyle()	

    h_gl_n1g.GetYaxis().SetTitleOffset(1.2)

    #tag for plots
    ptag=''
    if config.fullbr:
	ptag="_full"    

    #strings for decays
    gluino="#tilde{g}"
    to="#rightarrow"
    g="g"
    qq="q#bar{q}"
#    n1="#tilde{#chi}^{0}_{1}"
#    n2="#tilde{#chi}^{0}_{2}"
#    n3="#tilde{#chi}^{0}_{3}"
#    c1="#tilde{#chi}^{#pm}_{1}"
    n1="N_{1}"
    n2="N_{2}"
    n3="N_{3}"
    c1="C_{1}"
    grav="#tilde{G}"
    gamma="#gamma"
    zboson="Z"
    hboson="h"

    tab1=0.15
    tab2=0.192
    tab3=0.25

    gtab2=0.205
    qtab2=0.216
    
    tab3=0.26

    line1=0.84

    textsize=0.05
    mini=0.8 #80% reduction of text size

    if config.fullbr:
	    textsize=0.04

    #gl->chi10+g
    cv1 = TCanvas('cv1','',800,600)
    cv1.SetLeftMargin(0.1) 
    cv1.SetRightMargin(tab1)
    h_gl_n1g.Draw('colz')
    mu_axis.Draw()

    proc = TLatex(tab1,line1,gluino+to+g+n1)
    proc.SetTextSize(textsize) 
    proc.SetNDC()
    proc.Draw()

    cv1.SaveAs(config.outpath+"gl_n1g"+ptag+".eps")

    #gl->chi20+g
    c2 = TCanvas('c2','',800,600)
    c2.SetLeftMargin(0.1) 
    c2.SetRightMargin(tab1)
    h_gl_n2g.Draw('colz')
    mu_axis.Draw()

    proc = TLatex(tab1,line1,gluino+to+g+n2)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()
    if config.fullbr:
	    proc2 = TLatex(gtab2,line1-0.05,n2+to+n1)
	    proc2.SetTextSize(textsize) 
	    proc2.SetNDC()
	    proc2.Draw()
	    proc3 = TLatex(gtab2,line1-0.1,n2+to+c1+to+n1)
	    proc3.SetTextSize(textsize)
	    proc3.SetNDC()
	    proc3.Draw()
 
    
    c2.SaveAs(config.outpath+"gl_n2g"+ptag+".eps")

    #gl->chi30+g
    c3 = TCanvas('c3','',800,600)
    c3.SetLeftMargin(0.1) 
    c3.SetRightMargin(tab1)
    h_gl_n3g.Draw('colz')
    mu_axis.Draw()

    proc0 = TLatex(tab1,line1,gluino+to+g+n3)
    proc0.SetTextSize(textsize*mini)
    proc0.SetNDC()
    proc0.Draw()
    if config.fullbr:
	    proc1 = TLatex(0.195,0.8,n3+to+n1)
	    proc1.SetTextSize(textsize*mini) 
	    proc1.SetNDC()
	    proc1.Draw()
	    proc2 = TLatex( 0.195, 0.76,n3+to+n2)
	    proc2.SetTextSize(textsize*mini) 
	    proc2.SetNDC()
	    proc2.Draw()

	    proc21 = TLatex(0.236,0.72,n2+to+n1)
	    proc21.SetTextSize(textsize*mini) 
	    proc21.SetNDC()
	    proc21.Draw()
	    proc22 = TLatex(0.236,0.68,n2+to+c1+to+n1)
	    proc22.SetTextSize(textsize*mini) 
	    proc22.SetNDC()
	    proc22.Draw()

	    proc3 = TLatex(0.195,0.64,n3+to+c1+to+n1)
	    proc3.SetTextSize(textsize*mini)
	    proc3.SetNDC()
	    proc3.Draw()

    c3.SaveAs(config.outpath+"gl_n3g"+ptag+".eps")

    #gl->chi10+qq
    c4 = TCanvas('c4','',800,600)
    c4.SetLeftMargin(0.1) 
    c4.SetRightMargin(tab1)
    h_gl_n1qq.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+qq+n1)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()

    
    c4.SaveAs(config.outpath+"gl_n1qq"+ptag+".eps")

    #gl->chi20+qq
    c5 = TCanvas('c5','',800,600)
    c5.SetLeftMargin(0.1) 
    c5.SetRightMargin(tab1)
    h_gl_n2qq.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+qq+n2)
    proc.SetTextSize(textsize) 
    proc.SetNDC() 
    proc.Draw()
    if config.fullbr:
	    proc2 = TLatex(qtab2,line1-0.05,n2+to+n1)
	    proc2.SetTextSize(textsize) 
	    proc2.SetNDC()
	    proc2.Draw()
	    proc3 = TLatex(qtab2,line1-0.1,n2+to+c1+to+n1)
	    proc3.SetTextSize(textsize)
	    proc3.SetNDC()
	    proc3.Draw()
    
    c5.SaveAs(config.outpath+"gl_n2qq"+ptag+".eps")
    
    #gl->chi30+qq
    c6 = TCanvas('c6','',800,600)
    c6.SetLeftMargin(0.1) 
    c6.SetRightMargin(tab1)
    h_gl_n3qq.Draw('colz')
    mu_axis.Draw()
    
    proc0 = TLatex(tab1,line1,gluino+to+qq+n3)
    proc0.SetTextSize(textsize*mini) 
    proc0.SetNDC()
    proc0.Draw()
    if config.fullbr:
	    proc1 = TLatex(0.205,0.8,n3+to+n1)
	    proc1.SetTextSize(textsize*mini) 
	    proc1.SetNDC()
	    proc1.Draw()
	    proc2 = TLatex( 0.205, 0.76,n3+to+n2)
	    proc2.SetTextSize(textsize*mini) 
	    proc2.SetNDC()
	    proc2.Draw()

	    proc21 = TLatex(0.246,0.72,n2+to+n1)
	    proc21.SetTextSize(textsize*mini) 
	    proc21.SetNDC()
	    proc21.Draw()
	    proc22 = TLatex(0.246,0.68,n2+to+c1+to+n1)
	    proc22.SetTextSize(textsize*mini) 
	    proc22.SetNDC()
	    proc22.Draw()

	    proc3 = TLatex(0.205,0.64,n3+to+c1+to+n1)
	    proc3.SetTextSize(textsize*mini)
	    proc3.SetNDC()
	    proc3.Draw()
    
    c6.SaveAs(config.outpath+"gl_n3qq"+ptag+".eps")
    
    #gl->chi1+_ + qq
    c7 = TCanvas('c7','',800,600)
    c7.SetLeftMargin(0.1) 
    c7.SetRightMargin(tab1)
    h_gl_c1qq.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+qq+c1)
    if config.fullbr:
	    proc = TLatex(tab1,line1,gluino+to+qq+c1+to+n1)
    proc.SetTextSize(textsize) 
    proc.SetNDC() 
    proc.Draw()
    
    c7.SaveAs(config.outpath+"gl_c1qq"+ptag+".eps")
    
    #gl->~G + g
    c8 = TCanvas('c8','',800,600)
    c8.SetLeftMargin(0.1) 
    c8.SetRightMargin(tab1)
    h_gl_gravg.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+g+grav)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()
    
    c8.SaveAs(config.outpath+"gl_gravg"+ptag+".eps")

    #chi10->~G + gam
    c9 = TCanvas('c9','',800,600)
    c9.SetLeftMargin(0.1) 
    c9.SetRightMargin(tab1)
    h_n1_gravgam.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1-0.05,gluino+to+grav+gamma)
    proc.SetTextSize(textsize) 
    proc.SetNDC() 
    proc.Draw()

    c9.SaveAs(config.outpath+"n1_gravgam"+ptag+".eps")

    #chi10->~G + gam
    c10 = TCanvas('c10','',800,600)
    c10.SetLeftMargin(0.1) 
    c10.SetRightMargin(tab1)
    h_n1_gravz.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1-0.05,gluino+to+grav+zboson)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()
    
    c10.SaveAs(config.outpath+"n1_gravz"+ptag+".eps")
    
    #chi10->~G + gam
    c11 = TCanvas('c11','',800,600)
    c11.SetLeftMargin(0.1) 
    c11.SetRightMargin(tab1)
    h_n1_gravh.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1-0.05,gluino+to+grav+hboson)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()
    
    c11.SaveAs(config.outpath+"n1_gravh"+ptag+".eps")


    #gl->~chi10 (inclusive)
    c12 = TCanvas('c12','',800,600)
    c12.SetLeftMargin(0.1) 
    c12.SetRightMargin(tab1)
    h_gl_n1.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+n1)
    proc.SetTextSize(textsize)
    proc.SetNDC()
    proc.Draw()
    
    c12.SaveAs(config.outpath+"gl_n1"+ptag+".eps")

    #gl->~chi20 (inclusive)
    c13 = TCanvas('c13','',800,600)
    c13.SetLeftMargin(0.1) 
    c13.SetRightMargin(tab1)
    h_gl_n2.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+n2)
    proc.SetTextSize(textsize)  
    proc.SetNDC()
    proc.Draw()
    if config.fullbr:
	    proc2 = TLatex(tab2,line1-0.05,n2+to+n1)
	    proc2.SetTextSize(textsize) 
	    proc2.SetNDC()
	    proc2.Draw()
	    proc3 = TLatex(tab2,line1-0.1,n2+to+c1+to+n1)
	    proc3.SetTextSize(textsize)
	    proc3.SetNDC()
	    proc3.Draw()
    
    c13.SaveAs(config.outpath+"gl_n2"+ptag+".eps")

    #gl->~chi30 (inclusive)
    c14 = TCanvas('c14','',800,600)
    c14.SetLeftMargin(0.1) 
    c14.SetRightMargin(tab1)
    h_gl_n3.Draw('colz')
    mu_axis.Draw()
    
    proc0 = TLatex(tab1,line1,gluino+to+n3)
    proc0.SetTextSize(textsize*mini) 
    proc0.SetNDC()
    proc0.Draw()
    if config.fullbr:
	    proc1 = TLatex(0.18,0.8,n3+to+n1)
	    proc1.SetTextSize(textsize*mini) 
	    proc1.SetNDC()
	    proc1.Draw()
	    proc2 = TLatex( 0.18, 0.76,n3+to+n2)
	    proc2.SetTextSize(textsize*mini) 
	    proc2.SetNDC()
	    proc2.Draw()

	    proc21 = TLatex(0.224,0.72,n2+to+n1)
	    proc21.SetTextSize(textsize*mini) 
	    proc21.SetNDC()
	    proc21.Draw()
	    proc22 = TLatex(0.224,0.68,n2+to+c1+to+n1)
	    proc22.SetTextSize(textsize*mini) 
	    proc22.SetNDC()
	    proc22.Draw()

	    proc3 = TLatex(0.18,0.64,n3+to+c1+to+n1)
	    proc3.SetTextSize(textsize*mini)
	    proc3.SetNDC()
	    proc3.Draw()

	    
    c14.SaveAs(config.outpath+"gl_n3"+ptag+".eps")

    #gl->~chi1+ (inclusive)
    c15 = TCanvas('c15','',800,600)
    c15.SetLeftMargin(0.1) 
    c15.SetRightMargin(tab1)
    h_gl_c1.Draw('colz')
    mu_axis.Draw()
    
    proc = TLatex(tab1,line1,gluino+to+c1)
    if config.fullbr:
	    proc = TLatex(tab1,line1,gluino+to+c1+to+n1)
    proc.SetTextSize(textsize) 
    proc.SetNDC() 
    proc.Draw()
    
    c15.SaveAs(config.outpath+"gl_c1"+ptag+".eps")
