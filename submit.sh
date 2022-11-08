#!/bin/bash
#PBS -l nodes=1:ppn=2
#PBS -q batch
#PBS -N massbatch
#PBS -S /bin/bash
#PBS -m n
#PBS -V

echo "***********************************************************************"
echo " Starting job:"
echo "    Name:              "$PBS_JOBNAME
echo "    ID:                "$PBS_JOBID
echo "    Hostname:          "$PBS_O_HOST
echo "    Working directory: "$PBS_O_WORKDIR
echo "    Submitted using:   /opt/bin/sjob -p psi4 -d"
echo "***********************************************************************"

export TMPDIR=/tmp/$USER/$PBS_JOBID
export PSI_SCRATCH=/tmp/$USER/$PBS_JOBID
export OMP_NUM_THREADS=1
export NSLOTS=2

mkdir -p /tmp/$USER/$PBS_JOBID
cd $PBS_O_WORKDIR

/opt/miniconda3/envs/psi4/bin/psi4 -n 2 -i input.dat -o output.dat
/opt/miniconda3/envs/python2.7/bin/python /opt/scripts/sjob/qwrite $PBS_JOBID


