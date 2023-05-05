#!/bin/bash
#
# Script de exemplo para submeter trabalho que não use MPI
#
#SBATCH --job-name=NM1            # Nome do trabalho a ser executado (para melhor identificação)
#SBATCH --partition=open_cpu                  # Em qual fila o trabalho será executado (ver filas disponíveis com o comando sinfo)
#SBATCH --tasks-per-node=20
#SBATCH --nodes=1              # Número de nós (computadores) que serão utilizados (1 para códigos openMP)
#SBATCH --time=30-00:00:00                    # Tempo máximo de simulação (D-HH:MM). O tempo 00:00:00 corresponde a sem limite.
#SBATCH -o slurm.%N.%j.out                 # Nome do arquivo onde a saída (stdout) será gravada %N = Máquina , %j = Número do trabalho. 
#SBATCH -e slurm.%N.%j.err                    # Nome do arquivo para qual a saída de erros  (stderr) será redirecionada.
#SBATCH --mail-user=widmark.cardoso@teg.ufsc.br # Email para enviar notificações sobre alteração no estados do trabalho
#SBATCH --mail-type=BEGIN                  # Envia email quando o trabalho for iniciado
#SBATCH --mail-type=END                    # Envia email quando o trabalho finalizar
#SBATCH --mail-type=FAIL                   # Envia email caso o trabalho apresentar uma mensagem de erro.

module load gnu9
module load openmpi4
module load fftw
module load openfoam/2112_Int32

source $WM_PROJECT_DIR/bin/tools/RunFunctions

#cp -ar 0.org 0

# --- Gera malha
#runApplication gmshToFoam cylinderSourceOPT.msh
#runApplication gmshToFoam teste50ppw.msh
#runApplication gmshToFoam newMesh1.msh
#runApplication changeDictionary 
#runApplication blockMesh

#--- Paralelização
#runApplication decomposePar
#runParallel renumberMesh -overwrite
decomposePar > log.decomposePar

#--- Rodar simulação
runParallel myrhoCentralFoam

#--- Pós-processamento
runApplication reconstructPar
postProcess -func probesTime > log.postProcessTime
postProcess -latestTime -func probesSpacial > log.postProcessSpacial

