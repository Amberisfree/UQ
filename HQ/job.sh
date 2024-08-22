#! /bin/bash

#HQ --time-request=20s
#HQ --time-limit=10m
#HQ --stdout out.txt
#HQ --stderr err.txt
#HQ --nodes=2
# Launch model server, send back server URL
# and wait to ensure that HQ won't schedule any more jobs to this allocation.
module load gcc openmpi
unset SLURM_CPU_BIND SLURM_CPU_BIND_VERBOSE SLURM_CPU_BIND_LIST SLURM_CPU_BIND_TYPE

function get_avaliable_port {
    # Define the range of ports to select from
    MIN_PORT=1024
    MAX_PORT=65535

    # Generate a random port number
    port=$(shuf -i $MIN_PORT-$MAX_PORT -n 1)

    # Check if the port is in use
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; do
        # If the port is in use, generate a new random port number
        port=$(shuf -i $MIN_PORT-$MAX_PORT -n 1)
    done

    echo $port
}

port=$(get_avaliable_port)
export PORT=$port

# Assume that server sets the port according to the environment variable 'PORT'.
#SINGULARITYENV_PORT=$port
# mpirun -np 4 singularity run --no-home --writable /nobackup/mrfb78/workspace/opengo2 & # CHANGE ME!

#srun --overlap --ntasks-per-node=2 --ntasks=4 --cpus-per-task=1 --nodes=$HQ_NUM_NODES --nodefile=$HQ_NODE_FILE singularity run --no-home --writable /nobackup/mrfb78/workspace/opengo2 # CHANGE ME!
srun --overlap --ntasks-per-node=2 --ntasks=4 --cpus-per-task=2 --nodes=$HQ_NUM_NODES --nodefile=$HQ_NODE_FILE mpirun ./mpi-hello-world
load_balancer_dir="/nobackup/mrfb78/workspace/umbridge/hpc/" # CHANGE ME!


host=$(hostname -I | awk '{print $1}')

echo $host
echo $port
echo "Waiting for model server to respond at $host:$port..."
while ! curl -s "http://$host:$port/Info" > /dev/null; do
    sleep 1
done
echo "Model server responded"

# Write server URL to file identified by HQ job ID.
mkdir -p "$load_balancer_dir/urls"
echo "http://$host:$port" > "$load_balancer_dir/urls/url-$HQ_JOB_ID.txt"

sleep infinity # keep the job occupied