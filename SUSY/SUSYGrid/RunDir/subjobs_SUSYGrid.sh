#! /bin/sh

#Grid type choice
if [ -z $1 ] ; then
  echo "Please provide needed input! "
  echo ""
  echo "Usage :  "$0" grid_type <run_mode> <Hmass> <TanBeta> <YourTag>"
  echo ""
  echo "         grid_type   0=gl_neut , 1=sq_neut, 2=neut(EWK)"
  echo "         runmode     0=custom  , 1=scan , 2=Mgrav_scan (optional)"
  echo "         Hmass       in case you want to set the Higgs mass by hand [GeV] (optional) [just set by the model otherwise]"
  echo "         TanBeta     in case you want to set TanBeta by hand (1.5 by default)"
  echo "         YourTag     a tag of your choice for the output tar file (optional)"
  exit -1
fi

MYPATH=`echo $PWD`

#Running mode  [custom or scan]
RUNSCAN=0
if [ $# -gt 1 ] ; then
  RUNSCAN=$2
fi

HMASS=-999
if [ $# -gt 2 ] ; then
  HMASS=$3
fi

TANBETA=1.5
if [ $# -gt 3 ] ; then
  TANBETA=$4
fi

MYTAG=""
if [ $# -gt 4 ] ; then
  MYTAG=$5
fi

#QUEUE=8nh
QUEUE=1nd

TODAY=`date +"%m_%d_%y_%H_%M"`

bsub -q $QUEUE -o $MYPATH/logs/susyhit_$TODAY.log $MYPATH"/runSUSYGrid.sh "$1" "$RUNSCAN" "$HMASS" "$TANBETA" "$TODAY" "$MYTAG


