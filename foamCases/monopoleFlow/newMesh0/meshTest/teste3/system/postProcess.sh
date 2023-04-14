source /usr/lib/openfoam/openfoam2112/etc/bashrc

cat $FOAM_RUN

source $WM_PROJECT_DIR/bin/tools/RunFunctions

reconstructPar -time 2
reconstructPar -time 4

postProcess -time 2 -func probesTimeFlow10
postProcess -time 4 -func probesTimeFlow10