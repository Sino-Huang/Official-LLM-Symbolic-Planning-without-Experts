#!/bin/bash

#SBATCH --nodes=1

#SBATCH --ntasks=4

#SBATCH --cpus-per-task=2

#SBATCH --time=9-04:00:00

#SBATCH --mem=64G

#SBATCH --partition=deeplearn

#SBATCH -A punim0478

#SBATCH --gres=gpu:1

#SBATCH -q gpgpudeeplearn

#SBATCH --constraint=dlg5|dlg6

export PYTHONPATH=$PWD
export WORKING_DIR=$PWD
export TOKENIZERS_PARALLELISM=false

kedro run -p action_schema_combination --params use_cp=false
