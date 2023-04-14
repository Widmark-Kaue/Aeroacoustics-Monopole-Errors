#!/bin/bash

source /usr/lib/openfoam/openfoam2112/etc/bashrc

cat $FOAM_RUN

source $WM_PROJECT_DIR/bin/tools/RunFunctions


#foamCleanTutorials

#cp -ar ../../mesh/msh/teste50ppw.msh .

restore0Dir
runApplication gmshToFoam teste50ppw.msh
runApplication changeDictionary
runApplication decomposePar
runParallel renumberMesh -overwrite
runParallel $(getApplication) &


