#!/bin/bash

#define search patterns
s_M_1="# M_1"
s_M_3="# M_3"
s_mu="# mu(EWSB)"
s_msq="# M_q1L"

s_gl_width="# gluino decays"
s_gl_to_G="# BR(~g -> ~G      g)"
s_gl_to_chi10="# BR(~g -> ~chi_10 g)"
s_gl_to_chi20="# BR(~g -> ~chi_20 g)"

s_chi10_mass="# ~chi_10"
s_chi10_width="# neutralino1 decays"
s_chi10_to_Ggam="# BR(~chi_10 -> ~G        gam)"
s_chi10_to_GZ="# BR(~chi_10 -> ~G        Z)"
s_chi10_to_Gh="# BR(~chi_10 -> ~G        h)"

s_chi20_mass="# ~chi_20"
s_chi20_width="# neutralino2 decays"
s_chi20_to_Ggam="# BR(~chi_20 -> ~G        gam)"
s_chi20_to_GZ="# BR(~chi_20 -> ~G        Z)"
s_chi20_to_Gh="# BR(~chi_20 -> ~G        h)"
s_chi20_to="# BR(~chi_20 -> "

s_hmass="# h"

s_Gmass="# ~gravitino"

s_null="0.00000000E+00"

hbar=6.582E-25  #GeV.s
cspeed=2.99792458E8 #m.s

#initialize cumulative chi20 decay BRs
cum_chi20_d1=0
cum_chi20_d2=0
cum_chi20_d3=0

cum_chi20_d6=0
cum_chi20_d7=0
cum_chi20_d8=0
cum_chi20_d9=0
cum_chi20_d10=0
cum_chi20_d11=0
cum_chi20_d12=0
cum_chi20_d13=0
cum_chi20_d14=0
cum_chi20_d15=0
cum_chi20_d16=0
cum_chi20_d17=0
cum_chi20_d18=0
cum_chi20_d19=0
cum_chi20_d20=0
cum_chi20_d21=0
cum_chi20_d22=0
cum_chi20_d23=0
cum_chi20_d24=0
cum_chi20_d25=0
cum_chi20_d26=0
cum_chi20_d27=0

#get .out files
if [ -z $1 ] ; then
  echo "Expecting text file with paths."
  exit -1
fi

pathsFile="$1"

#OutputFile with extracted paramaters
if [ $# -gt 1 ] ; then
    OutFile='summary/SUSYGrid_out_pars_'$2'.dat'
else
    OutFile='summary/SUSYGrid_out_pars.dat'
fi

echo "#       M1            M3                mu          Msq         chi10_mass        BRtoGgam         BRtoGZ          BRtoGh           chi10Width     chi10Lenght     chi20_mass     chi20Width     chi20Lenght     chi20BRtoGgam        chi20BRtoGz        chi20BRtoGh        chi20BRdom_str        chi20BRdom        glWidth     glLenght     BRsgtochi10     BRsgtochi20     BRsgtoG        Hmass     Gmass" > $OutFile

L_d1=0
L_d2=0
L_d3=0
L_d6=0
L_d7=0
L_d8=0
L_d9=0
L_d10=0
L_d11=0
L_d12=0
L_d13=0
L_d14=0
L_d15=0
L_d16=0
L_d17=0
L_d18=0
L_d19=0
L_d20=0
L_d21=0
L_d22=0
L_d23=0
L_d24=0
L_d25=0
L_d26=0
L_d27=0
LINES=0

#loop over files
while read -r sample ; do

    LINES=$(( $LINES + 1 ))

    #extract M1
    #M1=$( echo $sample | awk -F"_" '{printf("%.2f",$2)}' )
    M1=$(grep "$s_M_1" $sample | head -1 | awk -F" " '{printf("%s",$2)}')
    if [[ "$M1" == "" ]]; then
	M1=$s_null
    fi
 
    #extract M3
    #M3=$( echo $sample | awk -F"_" '{printf("%.2f",$4)}' )
    M3=$(grep "$s_M_3" $sample | head -1 | awk -F" " '{printf("%s",$2)}')
    if [[ "$M3" == "" ]]; then
	M3=$s_null
    fi

    #extract mu
    #mu=$( echo $sample | awk -F"_" '{printf("%.2f",$6)}' )
    mu=$(grep "$s_mu" $sample | head -1 | awk -F" " '{printf("%s",$2)}')
    if [[ "$mu" == "" ]]; then
	mu=$s_null
    fi

    #extract Msq
    msq=$(grep "$s_msq" $sample | head -1 | awk -F" " '{printf("%s",$2)}')
    if [[ "$msq" == "" ]]; then
	msq=$s_null
    fi

    #extract gluino width
    gl_width=$(grep "$s_gl_width" $sample | awk -F" " '{printf("%s",$3)}')
    if [[ "$gl_width" == "" ]]; then
	gl_width=$s_null
    fi

    #compute gluino decay lenght (if width not null)
    if [[ "$gl_width" == *$s_null* ]]; then
	gl_lenght=-9999999
    else
	gl_lenght=$(awk -v a=$hbar -v b=$gl_width -v c=$cspeed  'BEGIN{print ((a / b) * c)}')
    fi

    #extract gluino decay to chi10+g
    gl_to_chi10=$(grep "$s_gl_to_chi10" $sample | awk -F" " '{printf("%s",$1)}')
    if [[ "$gl_to_chi10" == "" ]]; then
	gl_to_chi10=$s_null
    fi

    #extract gluino decay to chi20+g
    gl_to_chi20=$(grep "$s_gl_to_chi20" $sample | awk -F" " '{printf("%s",$1)}')
    if [[ "$gl_to_chi20" == "" ]]; then
	gl_to_chi20=$s_null
    fi

    #extract gluino direct decay to g+~G
    gl_to_G=$(grep "$s_gl_to_G" $sample | awk -F" " '{printf("%s",$1)}')
    if [[ "$gl_to_G" == "" ]]; then
	gl_to_G=$s_null
    fi

    #extract neutralino10 mass
    chi10_mass=$(grep "$s_chi10_mass" $sample | awk -F" " '{printf("%s",$2)}')
    if [[ "$chi10_mass" == "" ]]; then
	chi10_mass=$s_null
    fi

    #extract neutralino20 mass
    chi20_mass=$(grep "$s_chi20_mass" $sample | awk -F" " '{printf("%s",$2)}')
    if [[ "$chi20_mass" == "" ]]; then
	chi20_mass=$s_null
    fi

    #extract gravitino mass
    G_mass=$(grep "$s_Gmass" $sample | awk -F" " '{printf("%s",$2)}')
    if [[ "$G_mass" == "" ]]; then
	G_mass=$s_null
    fi

    #extract neutralino width
    chi10_width=$(grep "$s_chi10_width" $sample | awk -F" " '{printf("%s",$3)}')
    if [[ "$chi10_width" == "" ]]; then
	chi10_width=$s_null
    fi

    #compute neutralino decay lenght (if width not null)
    if [[ "$chi10_width" == *$s_null* ]]; then
	chi10_lenght=-9999999
    else
	chi10_lenght=$(awk -v a=$hbar -v b=$chi10_width -v c=$cspeed  'BEGIN{print ((a / b) * c)}')
    fi

    #extract neutralino BRs
    chi10_to_Ggam=$(grep "$s_chi10_to_Ggam" $sample | awk -F" " '{printf("%s",$1)}')
    chi10_to_GZ=$(grep "$s_chi10_to_GZ" $sample | awk -F" " '{printf("%s",$1)}')
    chi10_to_Gh=$(grep "$s_chi10_to_Gh" $sample | awk -F" " '{printf("%s",$1)}')

    if [[ "$chi10_to_Ggam" == "" ]]; then
	chi10_to_Ggam=$s_null
    fi
    if [[ "$chi10_to_GZ" == "" ]]; then
	chi10_to_GZ=$s_null
    fi
    if [[ "$chi10_to_Gh" == "" ]]; then
	chi10_to_Gh=$s_null
    fi

    #extract neutralino2 width
    chi20_width=$(grep "$s_chi20_width" $sample | awk -F" " '{printf("%s",$3)}')
    if [[ "$chi20_width" == "" ]]; then
	chi20_width=$s_null
    fi

    #compute neutralino2 decay lenght (if width not null)
    if [[ "$chi20_width" == *$s_null* ]]; then
	chi20_lenght=-9999999
    else
	chi20_lenght=$(awk -v a=$hbar -v b=$chi20_width -v c=$cspeed  'BEGIN{print ((a / b) * c)}')
    fi

    #extract neutralino2 BRs
    chi20_to_Ggam=$(grep "$s_chi20_to_Ggam" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_to_GZ=$(grep "$s_chi20_to_GZ" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_to_Gh=$(grep "$s_chi20_to_Gh" $sample | awk -F" " '{printf("%s",$1)}')

    if [[ "$chi20_to_Ggam" == "" ]]; then
	chi20_to_Ggam=$s_null
    fi

    #extract dominant neutralino2 decay
    checkstr=$(grep "$s_chi20_to" $sample | sort -k1,1g -n | tail -1 | awk -F" " '{printf("%s",$5)}')
    if [[ "$checkstr" == "#" ]]; then
	chi20_to_dom_str=$(grep "$s_chi20_to" $sample | sort -k1,1g -n | tail -1 | awk -F" " '{printf("%s|%s",$8,$9)}')
    else
	chi20_to_dom_str=$(grep "$s_chi20_to" $sample | sort -k1,1g -n | tail -1 | awk -F" " '{printf("%s|%s|%s",$9,$10,$11)}')
    fi
    chi20_to_dom=$(grep "$s_chi20_to" $sample | sort -k1,1g -n | tail -1 | awk -F" " '{printf("%s",$1)}')

    #extract higgs mass
    higgs_mass=$(grep "$s_hmass" $sample | head -1 | awk -F" " '{printf("%s",$2)}')
    if [[ "$higgs_mass" == "" ]]; then
        higgs_mass=$s_null
    fi

    #Save parameters in output file
    echo $M1'   '$M3'   '$mu'   '$msq'   '$chi10_mass'   '$chi10_to_Ggam'   '$chi10_to_GZ'   '$chi10_to_Gh'   '$chi10_width'   '$chi10_lenght'   '$chi20_mass'   '$chi20_width'   '$chi20_lenght'   '$chi20_to_Ggam'   '$chi20_to_GZ'   '$chi20_to_Gh'   '$chi20_to_dom_str'   '$chi20_to_dom'   '$gl_width'   '$gl_lenght'   '$gl_to_chi10'   '$gl_to_chi20'   '$gl_to_G'   '$higgs_mass'   '$G_mass >> $OutFile

    ## Extract chi20 decay BRs
    chi20_d1=$(grep "# BR(~chi_20 -> ~G        gam)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d2=$(grep "# BR(~chi_20 -> ~G        Z)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d5=$(grep "# BR(~chi_20 -> ~G        h)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d6=$(grep "# BR(~chi_20 -> ~chi_1+ nu_taub tau-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d7=$(grep "# BR(~chi_20 -> ~chi_1- nu_tau  tau+)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d8=$(grep "# BR(~chi_20 -> ~chi_1+ nu_eb   e-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d9=$(grep "# BR(~chi_20 -> ~chi_1- nu_e    e+)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d10=$(grep "# BR(~chi_20 -> ~chi_1+ nu_mub  mu-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d11=$(grep "# BR(~chi_20 -> ~chi_1- nu_mu   mu+)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d12=$(grep "# BR(~chi_20 -> ~chi_1- db      u)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d13=$(grep "# BR(~chi_20 -> ~chi_1+ ub      d)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d14=$(grep "# BR(~chi_20 -> ~chi_1- sb      c)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d15=$(grep "# BR(~chi_20 -> ~chi_1+ cb      s)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d16=$(grep "# BR(~chi_20 -> ~chi_10 gam)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d17=$(grep "# BR(~chi_20 -> ~chi_10 tau+    tau-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d18=$(grep "# BR(~chi_20 -> ~chi_10 e+      e-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d19=$(grep "# BR(~chi_20 -> ~chi_10 mu+     mu-)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d20=$(grep "# BR(~chi_20 -> ~chi_10 nu_eb   nu_e)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d21=$(grep "# BR(~chi_20 -> ~chi_10 nu_mub  nu_mu)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d22=$(grep "# BR(~chi_20 -> ~chi_10 nu_taub nu_tau)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d23=$(grep "# BR(~chi_20 -> ~chi_10 ub      u)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d24=$(grep "# BR(~chi_20 -> ~chi_10 cb      c)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d25=$(grep "# BR(~chi_20 -> ~chi_10 bb      b)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d26=$(grep "# BR(~chi_20 -> ~chi_10 db      d)" $sample | awk -F" " '{printf("%s",$1)}')
    chi20_d27=$(grep "# BR(~chi_20 -> ~chi_10 sb      s)" $sample | awk -F" " '{printf("%s",$1)}')

    TOTAL=0
    if [[ "$chi20_d1" != "" ]]; then
	cum_chi20_d1=$(awk -v a=$cum_chi20_d1 -v b=$chi20_d1 'BEGIN{print (a + b)}')    
	L_d1=$(( $L_d1 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d1 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d2" != "" ]]; then
	cum_chi20_d2=$(awk -v a=$cum_chi20_d2 -v b=$chi20_d2 'BEGIN{print (a + b)}')    
	L_d2=$(( $L_d2 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d2 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d3" != "" ]]; then
	cum_chi20_d3=$(awk -v a=$cum_chi20_d3 -v b=$chi20_d3 'BEGIN{print (a + b)}')    
	L_d3=$(( $L_d3 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d3 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d6" != "" ]]; then
	cum_chi20_d6=$(awk -v a=$cum_chi20_d6 -v b=$chi20_d6 'BEGIN{print (a + b)}')    
	L_d6=$(( $L_d6 + 1 ))	
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d6 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d7" != "" ]]; then
	cum_chi20_d7=$(awk -v a=$cum_chi20_d7 -v b=$chi20_d7 'BEGIN{print (a + b)}')    
	L_d7=$(( $L_d7 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d7 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d8" != "" ]]; then
	cum_chi20_d8=$(awk -v a=$cum_chi20_d8 -v b=$chi20_d8 'BEGIN{print (a + b)}')    
	L_d8=$(( $L_d8 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d8 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d9" != "" ]]; then
	cum_chi20_d9=$(awk -v a=$cum_chi20_d9 -v b=$chi20_d9 'BEGIN{print (a + b)}')    
	L_d9=$(( $L_d9 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d9 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d10" != "" ]]; then
	cum_chi20_d10=$(awk -v a=$cum_chi20_d10 -v b=$chi20_d10 'BEGIN{print (a + b)}')    
	L_d10=$(( $L_d10 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d10 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d11" != "" ]]; then
	cum_chi20_d11=$(awk -v a=$cum_chi20_d11 -v b=$chi20_d11 'BEGIN{print (a + b)}')    
	L_d11=$(( $L_d11 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d11 'BEGIN{print (a + b)}')    
    fi    

    if [[ "$chi20_d12" != "" ]]; then
	cum_chi20_d12=$(awk -v a=$cum_chi20_d12 -v b=$chi20_d12 'BEGIN{print (a + b)}')    
	L_d12=$(( $L_d12 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d12 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d13" != "" ]]; then
	cum_chi20_d13=$(awk -v a=$cum_chi20_d13 -v b=$chi20_d13 'BEGIN{print (a + b)}')    
	L_d13=$(( $L_d13 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d13 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d14" != "" ]]; then
	cum_chi20_d14=$(awk -v a=$cum_chi20_d14 -v b=$chi20_d14 'BEGIN{print (a + b)}')    
	L_d14=$(( $L_d14 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d14 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d15" != "" ]]; then
	cum_chi20_d15=$(awk -v a=$cum_chi20_d15 -v b=$chi20_d15 'BEGIN{print (a + b)}')    
	L_d15=$(( $L_d15 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d15 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d16" != "" ]]; then
	cum_chi20_d16=$(awk -v a=$cum_chi20_d16 -v b=$chi20_d16 'BEGIN{print (a + b)}')    
	L_d16=$(( $L_d16 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d16 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d17" != "" ]]; then
	cum_chi20_d17=$(awk -v a=$cum_chi20_d17 -v b=$chi20_d17 'BEGIN{print (a + b)}')    
	L_d17=$(( $L_d17 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d17 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d18" != "" ]]; then
	cum_chi20_d18=$(awk -v a=$cum_chi20_d18 -v b=$chi20_d18 'BEGIN{print (a + b)}')    
	L_d18=$(( $L_d18 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d18 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d19" != "" ]]; then
	cum_chi20_d19=$(awk -v a=$cum_chi20_d19 -v b=$chi20_d19 'BEGIN{print (a + b)}')    
	L_d19=$(( $L_d19 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d19 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d20" != "" ]]; then
	cum_chi20_d20=$(awk -v a=$cum_chi20_d20 -v b=$chi20_d20 'BEGIN{print (a + b)}')    
	L_d20=$(( $L_d20 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d20 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d21" != "" ]]; then
	cum_chi20_d21=$(awk -v a=$cum_chi20_d21 -v b=$chi20_d21 'BEGIN{print (a + b)}')    
	L_d21=$(( $L_d21 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d21 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d22" != "" ]]; then
	cum_chi20_d22=$(awk -v a=$cum_chi20_d22 -v b=$chi20_d22 'BEGIN{print (a + b)}')    
	L_d22=$(( $L_d22 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d22 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d23" != "" ]]; then
	cum_chi20_d23=$(awk -v a=$cum_chi20_d23 -v b=$chi20_d23 'BEGIN{print (a + b)}')    
	L_d23=$(( $L_d23 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d23 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d24" != "" ]]; then
	cum_chi20_d24=$(awk -v a=$cum_chi20_d24 -v b=$chi20_d24 'BEGIN{print (a + b)}')    
	L_d24=$(( $L_d24 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d24 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d25" != "" ]]; then
	cum_chi20_d25=$(awk -v a=$cum_chi20_d25 -v b=$chi20_d25 'BEGIN{print (a + b)}')    
	L_d25=$(( $L_d25 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d25 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d26" != "" ]]; then
	cum_chi20_d26=$(awk -v a=$cum_chi20_d26 -v b=$chi20_d26 'BEGIN{print (a + b)}')    
	L_d26=$(( $L_d26 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d26 'BEGIN{print (a + b)}')    
    fi    
    if [[ "$chi20_d27" != "" ]]; then
	cum_chi20_d27=$(awk -v a=$cum_chi20_d27 -v b=$chi20_d27 'BEGIN{print (a + b)}')    
	L_d27=$(( $L_d27 + 1 ))
	TOTAL=$(awk -v a=$TOTAL -v b=$chi20_d27 'BEGIN{print (a + b)}')    
    fi    
    
    # closure test
    cum_chi20_d28=$(awk -v a=$TOTAL -v b=1 'BEGIN{print (b - a)}')    
    
    #some printouts
    #echo '-----------------------------------------'
    #echo $sample
    #echo 'M1 = '$M1
    #echo 'M3 = '$M3
    #echo 'mu = '$mu
    #echo 
    #echo 'gl_width = '$gl_width' GeV'
    #echo 'gl_lenght = '$gl_lenght' m'
    #echo 'BR(gl --> chi10 + ~G) = '$gl_to_chi10
    #echo  
    #echo 'chi10_width = '$chi10_width' GeV'
    #echo 'chi10_lenght = '$chi10_lenght' m'
    #echo 'BR(chi10 --> ~G + gamma) = '$chi10_to_Ggam
    #echo 'BR(chi10 --> ~G + Z) = '$chi10_to_GZ
    #echo 'BR(chi10 --> ~G + h) = '$chi10_to_Gh
    #echo 

done < <(ls $pathsFile/M1*.out)

cum_chi20_d1=$(awk -v a=$cum_chi20_d1 -v b=$L_d1 'BEGIN{print (a / b)}')    
cum_chi20_d2=$(awk -v a=$cum_chi20_d2 -v b=$L_d2 'BEGIN{print (a / b)}')    
cum_chi20_d3=$(awk -v a=$cum_chi20_d3 -v b=$L_d3 'BEGIN{print (a / b)}')    
cum_chi20_d6=$(awk -v a=$cum_chi20_d6 -v b=$L_d6 'BEGIN{print (a / b)}')    
cum_chi20_d7=$(awk -v a=$cum_chi20_d7 -v b=$L_d7 'BEGIN{print (a / b)}')    
cum_chi20_d8=$(awk -v a=$cum_chi20_d8 -v b=$L_d8 'BEGIN{print (a / b)}')    
cum_chi20_d9=$(awk -v a=$cum_chi20_d9 -v b=$L_d9 'BEGIN{print (a / b)}')    
cum_chi20_d10=$(awk -v a=$cum_chi20_d10 -v b=$L_d10 'BEGIN{print (a / b)}')    
cum_chi20_d11=$(awk -v a=$cum_chi20_d11 -v b=$L_d11 'BEGIN{print (a / b)}')    
cum_chi20_d12=$(awk -v a=$cum_chi20_d12 -v b=$L_d12 'BEGIN{print (a / b)}')    
cum_chi20_d13=$(awk -v a=$cum_chi20_d13 -v b=$L_d13 'BEGIN{print (a / b)}')    
cum_chi20_d14=$(awk -v a=$cum_chi20_d14 -v b=$L_d14 'BEGIN{print (a / b)}')    
cum_chi20_d15=$(awk -v a=$cum_chi20_d15 -v b=$L_d15 'BEGIN{print (a / b)}')    
cum_chi20_d16=$(awk -v a=$cum_chi20_d16 -v b=$L_d16 'BEGIN{print (a / b)}')    
cum_chi20_d17=$(awk -v a=$cum_chi20_d17 -v b=$L_d17 'BEGIN{print (a / b)}')    
cum_chi20_d18=$(awk -v a=$cum_chi20_d18 -v b=$L_d18 'BEGIN{print (a / b)}')    
cum_chi20_d19=$(awk -v a=$cum_chi20_d19 -v b=$L_d19 'BEGIN{print (a / b)}')    
cum_chi20_d20=$(awk -v a=$cum_chi20_d20 -v b=$L_d20 'BEGIN{print (a / b)}')    
cum_chi20_d21=$(awk -v a=$cum_chi20_d21 -v b=$L_d21 'BEGIN{print (a / b)}')    
cum_chi20_d22=$(awk -v a=$cum_chi20_d22 -v b=$L_d22 'BEGIN{print (a / b)}')    
cum_chi20_d23=$(awk -v a=$cum_chi20_d23 -v b=$L_d23 'BEGIN{print (a / b)}')    
cum_chi20_d24=$(awk -v a=$cum_chi20_d24 -v b=$L_d24 'BEGIN{print (a / b)}')    
cum_chi20_d25=$(awk -v a=$cum_chi20_d25 -v b=$L_d25 'BEGIN{print (a / b)}')    
cum_chi20_d26=$(awk -v a=$cum_chi20_d26 -v b=$L_d26 'BEGIN{print (a / b)}')    
cum_chi20_d27=$(awk -v a=$cum_chi20_d27 -v b=$L_d27 'BEGIN{print (a / b)}')    
cum_chi20_d28=$(awk -v a=$cum_chi20_d27 -v b=$LINES 'BEGIN{print (a / b)}')    

echo  "#" >> $OutFile
echo  "#" >> $OutFile
echo  "#" >> $OutFile
echo  "#" >> $OutFile
echo  "#### AVERAGE CHI20 DECAY BRs #####" >> $OutFile
echo  "####" >> $OutFile
echo  "#### BR(~chi_20 -> ~G        gam)           = "  $cum_chi20_d1 >> $OutFile
echo  "#### BR(~chi_20 -> ~G        Z)             = "  $cum_chi20_d2 >> $OutFile
echo  "#### BR(~chi_20 -> ~G        h)             = "  $cum_chi20_d3 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1+ nu_taub tau-)    = "  $cum_chi20_d6 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1- nu_tau  tau+)    = "  $cum_chi20_d7 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1+ nu_eb   e-)      = "  $cum_chi20_d8 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1- nu_e    e+)      = "  $cum_chi20_d9 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1+ nu_mub  mu-)     = "  $cum_chi20_d10 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1- nu_mu   mu+)     = "  $cum_chi20_d11 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1- db      u)       = "  $cum_chi20_d12 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1+ ub      d)       = "  $cum_chi20_d13 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1- sb      c)       = "  $cum_chi20_d14 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_1+ cb      s)       = "  $cum_chi20_d15 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 gam)             = "  $cum_chi20_d16 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 tau+    tau-)    = "  $cum_chi20_d17 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 e+      e-)      = "  $cum_chi20_d18 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 mu+     mu-)     = "  $cum_chi20_d19 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 nu_eb   nu_e)    = "  $cum_chi20_d20 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 nu_mub  nu_mu)   = "  $cum_chi20_d21 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 nu_taub nu_tau)  = "  $cum_chi20_d22 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 ub      u)       = "  $cum_chi20_d23 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 cb      c)       = "  $cum_chi20_d24 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 bb      b)       = "  $cum_chi20_d25 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 db      d)       = "  $cum_chi20_d26 >> $OutFile
echo  "#### BR(~chi_20 -> ~chi_10 sb      s)       = "  $cum_chi20_d27 >> $OutFile
echo  "#### BR(~chi_20 -> OTHER)                   = "  $cum_chi20_d28 >> $OutFile