#!/bin/bash
source /usr/lib/openfoam/openfoam2112/etc/bashrc

cat $FOAM_RUN
source $WM_PROJECT_DIR/bin/tools/RunFunctions

foamCleanTutorials

restore0Dir
runApplication blockMesh
runApplication changeDictionary
runApplication decomposePar
runParallel renumberMesh -overwrite
runParallel $(getApplication) &
