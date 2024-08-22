# QMCPy with UM-Bridge model demo


This is a demo for running QMCPy with UM-Bridge model on HPC.

# Introduction
This project explores the computational efficiency of
Quasi-Monte Carlo methods for quantifying uncertainty 
in Reservoir Engineering, specifically within the 
European North Sea regions. By applying a robust Uncertainty Quantification (UQ) framework developed by UM-Bridge, we utilized High-Performance Computing (HPC) systems to analyze large-scale synthetic data generated by the
Fortran model.

Our primary focus was on evaluating the influence of
uncertainty on various parameters using established 
benchmarks, including probabilistic analyses of algorithms.
We collaborated closely with industry partners OpenGo Simulations to enhance their subsurface carbon dioxide storage software.




# 1. Install dependencies
## Pull Dockerfile and Build the Docker image 

``` bash
sudo docker build -t opengo .&&
docker image save opengo -o opengo.tar &&
scp opengo.tar hamilton:/nobackup/[username]/workspace
```


## Build the Singularity image 
``` bash
module load singularity
singularity --version
SINGULARITY_CACHEDIR=$NOBACKUP singularity build --sandbox opengo docker-archive://opengo.tar 
```

## Get HQ
``` bash
wget https://github.com/It4innovations/hyperqueue/releases/download/v0.19.0/hq-v0.19.0-linux-x64.tar.gz
```
``` bash
tar -xzf hq-v0.19.0-linux-x64.tar.gz
```


# 2. Run the UM-Bridge HPC server with HQ
## Run the server by executing the following command of Load Balancer
## Using MPI platform: openMPI
``` bash
module load gcc openmpi
```
``` bash
cd /umbridge/hpc
```
``` bash
export PATH=$(pwd):$PATH &&
PORT=[4242] ./load-balancer
```

## Run the client
``` bash
python3 qmcpy-client.py http://localhost:[4242]
```

# 4. Some useful commands for Debugging

## Some useful commands for HQ
``` bash
./hq alloc list
```
``` bash
sacct -o jobid,elapsed,reqcpus -j [10618772]
```
``` bash
sinfo --help
```
``` bash
ls urls
```
``` bash
nano umbridge/hpc/hq_scripts/job.sh
```
``` bash
nano umbridge/hpc/hq_scripts/allocation_queue.sh
```

## Some useful commands for Singularity
``` bash
singularity shell --writable opengo
PORT=[4242] singularity run --no-home --writable opengo
```

## some useful commands for HPC
``` bash
squeue -u [username]
scancel id [jobid]
srun -p shared --pty /bin/bash
module load gcc openmpi
module list
```


# Reference


### Python QMCPy
https://qmcpy.readthedocs.io/en/master/index.html

### UM-Bridge HPC Server
https://um-bridge-benchmarks.readthedocs.io/en/docs/umbridge/hpc.html

### HyperQueue 
https://it4innovations.github.io/hyperqueue/stable/jobs/multinode/#running-mpi-tasks

### Pflotran OPENGO Geo-physics Model
https://docs.opengosim.com/

### Slurm and Hamilton
https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-supercomputer/usage/jobs/





