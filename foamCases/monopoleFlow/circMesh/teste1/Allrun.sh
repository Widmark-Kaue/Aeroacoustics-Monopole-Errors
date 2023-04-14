#!/bin/bash
source /usr/lib/openfoam/openfoam2112/etc/bashrc

cat $FOAM_RUN
source $WM_PROJECT_DIR/bin/tools/RunFunctions

foamCleanTuturials
cp -ar system/cylinderSourceOPT.msh .

restore0Dir
runApplication gmshToFoam cylinderSourceOPT.msh
runApplication changeDictionary
runApplication decomposePar
runParallel renumberMesh -overwrite
runParallel $(getApplication) &
