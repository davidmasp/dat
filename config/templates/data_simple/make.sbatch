#!/bin/bash

#SBATCH --job-name=data_simple_job
#SBATCH --mail-type=ALL
#SBATCH --mail-user=name.surname@company.com
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

# #SBATCH --partition=cpuq
# #SBATCH --mem-per-cpu=2G

#SBATCH --output=.log_%j.log
#SBATCH --error=.log_%j.log

# source .env
just all
