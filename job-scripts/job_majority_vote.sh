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


kedro run -p generate_schema_pool --params general.query_domain=libraryworld,general.desc_granularity=detailed &

kedro run -p generate_schema_pool --params general.query_domain=libraryworld,general.desc_granularity=layman &


kedro run -p generate_schema_pool --params general.query_domain=minecraft,general.desc_granularity=detailed &

kedro run -p generate_schema_pool --params general.query_domain=minecraft,general.desc_granularity=layman &


kedro run -p generate_schema_pool --params general.query_domain=rpggame,general.desc_granularity=detailed &

kedro run -p generate_schema_pool --params general.query_domain=rpggame,general.desc_granularity=layman &

wait