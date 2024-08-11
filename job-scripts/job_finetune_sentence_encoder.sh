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
export SENTENCE_TRANSFORMERS_HOME=$PWD


kedro run -p finetuning_sentence_encoder --params finetuning_encoder_cfg.train_batch_size=16,setup_sentence_encoder_cfg.model_name=sentence-transformers/all-roberta-large-v1,setup_sentence_encoder_cfg.model_type=bi_encoder,finetuning_encoder_cfg.is_finetune_complete=false,finetuning_encoder_cfg.train_batch_size=256