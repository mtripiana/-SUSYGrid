#!/bin/bash

## CONFIG PATHS

BASEPATH=`dirname $PWD`

SUSYOUTPATH=$BASEPATH"/RunDir/output/SLHA/"

###

#Grid type choice
if [ -z $1 ] ; then
  echo "Please specify what kind of grid you like to generate!! 0=gl_neut , 1=sq_neut , 2=neut(EWK)"
  echo "Usage :  "$0" grid_type <run_mode> <Hmass> <TanBeta> <Date> <YourTag>"
  echo ""	
  echo "         grid_type   0=gl_neut , 1=sq_neut, 2=neut(EWK)"
  echo "         runmode     0=custom  , 1=scan  (optional)"
  echo "         Hmass       in case you want to set the Higgs mass by hand [GeV] (optional) [just set by the model otherwise]"
  echo "         TanBeta     in case you want to set TanBeta by hand (1.5 by default)"
  echo "         Date        current date to tag output tar file (optional) [TODAY by default]"
  echo "         YourTag     a tag of your choice for the output tar file (optional)"
  exit -1
fi

#Running mode  [custom or scan]
FTAG=""
MYTAG=""
if [ $# -gt 1 ];then
    if [ $2 -eq 1 ];then
	echo "RUNNING IN SCAN MODE!"
	FTAG="_scan"
    fi
    if [ $2 -eq 2 ];then
	echo "RUNNING IN M(gravitino) SCAN MODE!"
	FTAG="_mGravScan"
    fi
    if [ $# -gt 5 ];then
	MYTAG=$6
    fi
fi


# for tracking when and where you run
hostname
date

echo ' '
# make a tmp working directory
tmpDir=`mktemp -d`
cd $tmpDir
echo 'temp dir: ' $tmpDir

echo ' '
echo ' Copying code...'
mkdir SUSYHIT
cd SUSYHIT

#copy working dirs
cp -r $BASEPATH/*.in .
cp -r $BASEPATH/*.f .
cp -r $BASEPATH/*.o .
cp -r $BASEPATH/makefile .
cp -r $BASEPATH/SuSpect .
cp -r $BASEPATH/run .
cp -r $BASEPATH/RunDir/scripts/Add* .
cp -r $BASEPATH/RunDir/scripts/Fix* .

#compile SuSpect 
cd SuSpect
source compileit.sh

#Back to SUSYHIT directory
cd ../

#Create running directories
mkdir -p RunDir/

#Run directory
cd RunDir/

RUNDIR=`pwd`
echo ''
echo 'Running in '$PWD

cp $BASEPATH/RunDir/python/writeSuspectPar.py .

###  CONFIGURE VARIABLES
CONFIGFILE=my_grid_points_to_run.txt
echo ' '
echo ' Creating configurations file '

cp $BASEPATH/RunDir/python/SUSYHIT_SinglePhotonGrid_makeconfigfile$FTAG.py SUSYHIT_SinglePhotonGrid_makeconfigfile.py

./SUSYHIT_SinglePhotonGrid_makeconfigfile.py $CONFIGFILE $1 $3 $4

#create output dir
mkdir -p $SUSYOUTPATH

cat $CONFIGFILE

#run over all grid points
Progress=0
while read -r sample ; do
#f=open($CONFIGFILE,'r')
#for sample in f.readline():    
    cd $RUNDIR

    m1=$(echo $sample | awk -F" " '{printf("%s",$1)}')    
    mu=$(echo $sample | awk -F" " '{printf("%s",$2)}')    
    m3=$(echo $sample | awk -F" " '{printf("%s",$3)}')    
    msq=$(echo $sample | awk -F" " '{printf("%s",$4)}')    
    at=$(echo $sample | awk -F" " '{printf("%s",$5)}')    
    Gmass=$(echo $sample | awk -F" " '{printf("%s",$6)}')    
    proc=$(echo $sample | awk -F" " '{printf("%s",$7)}')    
    gtype=$(echo $sample | awk -F" " '{printf("%s",$8)}')    
    Hmass=$(echo $sample | awk -F" " '{printf("%s",$9)}')    
    tanBeta=$(echo $sample | awk -F" " '{printf("%s",$10)}')    

    customGmass=$(awk -vx=$Gmass -vy="0.00" 'BEGIN{ print x>=y?1:0}')
    customHmass=$(awk -vx=$Hmass -vy="0.00" 'BEGIN{ print x>=y?1:0}')

    if [ "$customGmass" -eq 1 ];then
	if [ "$gtype" == "0" ];then
	    outfile='M1_'$(printf "%.2f" $m1)'_M3_'$(printf "%.2f" $m3)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'_Gmass_'$proc'.out'
	elif [ "$gtype" == "1" ];then
	    outfile='M1_'$(printf "%.2f" $m1)'_Msq_'$(printf "%.2f" $msq)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'_Gmass_'$proc'.out'
	else
	    outfile='M1_'$(printf "%.2f" $m1)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'_Gmass_'$proc'.out'
	fi
    else
	if [ "$gtype" == "0" ];then
	    outfile='M1_'$(printf "%.2f" $m1)'_M3_'$(printf "%.2f" $m3)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'.out'
	elif [ "$gtype" == "1" ];then
	    outfile='M1_'$(printf "%.2f" $m1)'_Msq_'$(printf "%.2f" $m3)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'.out'
	else
	    outfile='M1_'$(printf "%.2f" $m1)'_mu_'$(printf "%.2f" $mu)'_At_'$(printf "%.2f" $at)'_tanB_'$(printf "%.2f" $tanBeta)'.out'
	fi
    fi

    python writeSuspectPar.py $m1 $m3 $mu $msq $at $tanBeta

    #run SuSpect
    cd ../SuSpect

    ./suspect2

    #make SuSpect .out file the .in file for SUSYHIT run
    cp suspect2_lha.out ../slhaspectrum.in

    #go to SUSYHIT directory
    cd ../

    #hack MODSEL (to make it 'look like' GMSB)                                                                                                  
    sed -i 's/.*general MSSM.*/     1   2    #GMSB/' slhaspectrum.in

    #Fix ~t_1 mass (if needed)
    if [ "$gtype" == "1" ];then
	./FixT1mass slhaspectrum.in $msq
    fi

    #add the gravitino by hand!    
    if [ "$customGmass" -eq 1 ];then
	./AddGravitino slhaspectrum.in $Gmass
    else
	./AddGravitino slhaspectrum.in 5E-10
#	./AddGravitino slhaspectrum.in 5E-7
    fi

    #Fix Higgs mass (if needed)
    if [ "$customHmass" -eq 1 ];then
	./FixHiggs slhaspectrum.in $Hmass
    fi

    #compile SUSYHIT
    if [ $Progress -eq 0 ];then
	make -f makefile
    fi

    echo ' '
    echo 'compilation was fine '
    echo ' '

    #run SUSYHIT
    date
    echo ' Launching SUSYHIT ...'
    ./run
    date

    cp susyhit_slha.out $outfile

    ((Progress++))
    echo $Progress

done <$CONFIGFILE

#extract parameters from generated files
cp -r $BASEPATH/RunDir/scripts/ExtractParameters.sh .
mkdir summary
./ExtractParameters.sh . 

#save outputfile 
TODAY=$5

if [ "$gtype" == "0" ];then
    TAG="_gl_neut_"
elif [ "$gtype" == "1" ];then
    TAG="_sq_neut_"
else
    TAG="_neut_"
fi

echo ' '
echo ' copying back data to '$SUSYOUTPATH/SUSYGRID$TAG$TODAY$MYTAG.tar.gz

tar zcfv $SUSYOUTPATH/SUSYGRID$TAG$TODAY$MYTAG.tar.gz M1*out summary/*dat

cd $BASEPATH/RunDir
#echo 'we are back in '${PWD}
rm -rf ${tmpDir}
echo 'Cleanup done!'
date
