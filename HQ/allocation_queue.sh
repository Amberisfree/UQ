#! /bin/bash

# Note: For runs on systems without SLURM, replace the slurm allocator by
# ./hq worker start &


./hq alloc add slurm --time-limit 15m \
                   --idle-timeout 5m \
                   --backlog 1 \
                   --workers-per-alloc 1 \
                   --max-worker-count 32 \
                   --cpus=4 \
                   -- -p "shared" --mem "1500" # Add any neccessary SLURM arguments
# Any parameters after -- will be passed directly to sbatch (e.g. credentials, partition, mem, etc.)
