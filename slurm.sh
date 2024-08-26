#!/bin/bash
#SBATCH --nodes=2
#SBATCH --job-name=mixed
#SBATCH --ntasks=2 //1+1
#SBATCH --cpus-per-task=8
#SBATCH --mem=12G
#SBATCH --time=03:30:00
#SBATCH -p shared
#SBTACH -o multi.out
#SBATCH -o multi.err

#Put this file inside umbridge/hpc/

module purge
module load gcc openmpi python/3.10.8 valgrind

pip3 install qmcpy umbridge

function get_available_port {
    MIN_PORT=1024
    MAX_PORT=65535
    port=$(shuf -i $MIN_PORT-$MAX_PORT -n 1)
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; do
        port=$(shuf -i $MIN_PORT-$MAX_PORT -n 1)
    done
    echo $port
}

port=$(get_available_port)
echo "Selected port: $port"

export PATH=$(pwd):$PATH
export HQ_SUBMIT_DELAY_MS=50
export PORT=$port

# Capture the node running the load balancer
LOAD_BALANCER_NODE=$(srun --nodes=1 --ntasks=1 hostname)
echo "Load balancer will run on node: $LOAD_BALANCER_NODE"


srun --overlap --nodes=1 --ntasks=1 --output=server.out --error=server.err ./load-balancer &

sleep 30
echo "Waiting for model server to respond at $LOAD_BALANCER_NODE:$port"
#while ! curl -H "Connection: close" -s "http://$LOAD_BALANCER_NODE:$port/Info" > /dev/null; do
#    sleep 3
#    echo "Still waiting"
#done
echo "Model server responded"

loadbalancer_pid=$(lsof -t -i :$port)

function cleanup {
    echo "Cleaning up..."
    kill -SIGQUIT $loadbalancer_pid
    wait $loadbalancer_pid
    echo "Completed cleaning up"
}
trap cleanup EXIT

export MODEL_URL="http://$LOAD_BALANCER_NODE:$port"
export PYTHONUNBUFFERED=1
echo "Running the client with URL: $MODEL_URL"



# Start the client on the second node
echo "Starting client..."

srun --nodes=1 --ntasks=1 --output=client.out --error=client.err python3 qmcpy-client.py http://$LOAD_BALANCER_NODE:$port