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


# kedro run -p tree_of_thought_direct_planning --params general.query_domain=libraryworld,general.desc_granularity=detailed,\
# tot_direct_planning_cfg.model_name=gpt-4o-2024-05-13,tot_direct_planning_cfg.model_type=openai,\
# tot_direct_planning_cfg.tree_breadth=3

kedro run -p tree_of_thought_direct_planning --params general.query_domain=libraryworld,general.desc_granularity=detailed,\
tot_direct_planning_cfg.model_name=gpt-3.5-turbo-0125,tot_direct_planning_cfg.model_type=openai,\
tot_direct_planning_cfg.tree_breadth=3,tot_direct_planning_cfg.top_p=0.3,tot_direct_planning_cfg.temperature=0.4