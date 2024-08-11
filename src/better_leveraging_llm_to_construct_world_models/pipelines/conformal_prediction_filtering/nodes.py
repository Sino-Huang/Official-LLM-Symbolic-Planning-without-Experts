"""
This is a boilerplate pipeline 'conformal_prediction_filtering'
generated using Kedro 0.19.6
"""

import logging
import sys
import traceback
from datetime import datetime
import os
import torch.nn.functional as F
from datasets import load_dataset
from datasets import Dataset
from sentence_transformers import SentenceTransformer, losses, CrossEncoder
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.similarity_functions import SimilarityFunction
from sentence_transformers.trainer import SentenceTransformerTrainer
from sentence_transformers.training_args import BatchSamplers, SentenceTransformerTrainingArguments
from pathlib import Path
from tqdm.auto import tqdm 
from icecream import ic

from better_leveraging_llm_to_construct_world_models.pipelines.compare_cos_sim_between_act_and_nl_desc.nodes import COMPARING_SETTING, PAIR_TYPE
import torch as th
import seaborn as sns 
from copy import deepcopy
import json
import random
from typing import Sequence
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 
from glob import glob 
from pddl.parser.domain import DomainParser
from enum import Enum
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect

from better_leveraging_llm_to_construct_world_models.pipelines.finetuning_sentence_encoder.finetune_dataset import create_test_dataset
from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str

from better_leveraging_llm_to_construct_world_models.pipelines.setup_sentence_encoder.nodes import create_sentence_encoder_helper
from transformers import TrainerCallback

# ! NODE 
def calculate_cp_threshold(setup_sentence_encoder_cfg, finetuning_encoder_cfg, conformal_prediction_filtering_cfg, cosine_sim_comparison_data):
    model_name = setup_sentence_encoder_cfg['model_name']
    alpha = conformal_prediction_filtering_cfg['alpha']
    model_type = setup_sentence_encoder_cfg['model_type']
    if finetuning_encoder_cfg['best_model_path'] is not None:
        best_model_path = os.path.join(os.environ['WORKING_DIR'], finetuning_encoder_cfg['best_model_path'])
        if model_type == "bi_encoder":
            sentence_model = SentenceTransformer(best_model_path)
        elif model_type == "cross_encoder":
            sentence_model = CrossEncoder(best_model_path)
        checkpoint_tag = os.path.basename(os.path.dirname(finetuning_encoder_cfg['best_model_path']))
        print(f"checkpoint_tag: {checkpoint_tag}")
        
    else:
        raise ValueError('best_model_path is None')
    
    test_dataset = create_test_dataset(cosine_sim_comparison_data)
    test_output_dict= {
        'Domain' : [],
        'Action Name' : [],
        'Pair Type' : [],
        'Comparison Mode' : [],
        'Query Content' : [],
        'Answer Content' : [],
        'Cosine Sim Score' : []
    }
    query_text = []
    answer_text = []
    for test_data in tqdm(test_dataset, desc="Evaluating on test dataset"):
        domain = test_data['Domain']
        action_name = test_data['Action Name']
        pair_type = test_data['Pair Type']
        comparison_mode = test_data['Comparison Mode']
        query_content = test_data['Query Content']
        answer_content = test_data['Answer Content']
        test_output_dict['Domain'].append(domain)
        test_output_dict['Action Name'].append(action_name)
        test_output_dict['Pair Type'].append(pair_type)
        test_output_dict['Comparison Mode'].append(comparison_mode)
        test_output_dict['Query Content'].append(query_content)
        test_output_dict['Answer Content'].append(answer_content)
        query_text.append(query_content)
        answer_text.append(answer_content)
        
    chunksize = 32
    for i in range(0, len(query_text), chunksize):
        query_chunk = query_text[i:i+chunksize]
        answer_chunk = answer_text[i:i+chunksize]
        query_embedding = sentence_model.encode(query_chunk, convert_to_tensor=True)
        answer_embedding = sentence_model.encode(answer_chunk, convert_to_tensor=True)
        with th.no_grad():
            similarity_scores = F.cosine_similarity(query_embedding, answer_embedding)
        for j, score in enumerate(similarity_scores):
            test_output_dict['Cosine Sim Score'].append(score.item())
            
    # form the dataframe
    validation_set_testing_output_df = pd.DataFrame(test_output_dict)
    
    # only consider the "Positive (Correct Match)"" pairs and comparison mode is "NL Desc vs. Action Schema"
    cond1 = validation_set_testing_output_df['Comparison Mode'] == "NL Desc vs. Action Schema"
    cond2 = validation_set_testing_output_df['Pair Type'] == "Positive (Correct Match)"
    filtered_df = validation_set_testing_output_df[cond1 & cond2]
    assert len(filtered_df) > 0, "No positive pairs found"
    # get cosine similarity score
    cal_array = filtered_df['Cosine Sim Score'].values.tolist()
    # calculate the threshold
    threshold_val = calculate_threshold(cal_array, alpha)
    # make it a dict to have more information 
    cp_threshold_dict = {
        'threshold_val': threshold_val,
        'alpha': alpha,
        'model_name': model_name,
        'checkpoint_tag': checkpoint_tag
    }
    output_data = [cp_threshold_dict]
    for i in range(2):
        alpha_u = alpha + (i+1) * 0.1
        threshold_val = calculate_threshold(cal_array, alpha_u)
        cp_threshold_dict = {
            'threshold_val': threshold_val,
            'alpha': alpha_u,
            'model_name': model_name,
            'checkpoint_tag': checkpoint_tag
        }
        output_data.append(cp_threshold_dict)
    
    return output_data
    
    
    
def calculate_threshold(cal_array, alpha):
    # Quantile-based Thresholding for Conformal Prediction
    # score vector shape [N, M], where the N is the batch number, and the M is actually the number of classes, however, in our case, we are doing the cosine similarity, so the M is the number of text batch, which is the same as the vision batch
    cal_array = np.asarray(cal_array)

    n = len(cal_array)
    cal_scores = 1 - cal_array # get the score of the correct label, the score is 1 - cosine similarity

    # ! 2: get adjusted quantile
    q_level = np.ceil((n+1) * (1-alpha))/n
    qhat = np.quantile(cal_scores, q_level, method="higher")
    threshold = 1 - qhat

    return threshold