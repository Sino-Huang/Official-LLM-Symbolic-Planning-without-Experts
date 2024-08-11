"""
This is a boilerplate pipeline 'post_construction_ranking'
generated using Kedro 0.19.6
"""
from copy import deepcopy
import json
import random
import numpy as np
from typing import Sequence
from sentence_transformers import SentenceTransformer, CrossEncoder
import torch
from tqdm.auto import tqdm
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
from pathlib import Path
import os 
from glob import glob 
from pddl.parser.domain import DomainParser
from enum import Enum
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect
import itertools
from pddl.formatter import domain_to_string, problem_to_string
import multiprocessing as mp
from multiprocessing import Pool, Manager, Lock
import torch.nn.functional as F
from tqdm.contrib.concurrent import process_map
from collections import defaultdict

from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str
from natsort import natsorted
import re

# ! NODE
def generate_plans_with_scores(general_cfg, setup_sentence_encoder_cfg, finetuning_encoder_cfg, post_construction_ranking_cfg):
    if "solver_url" in post_construction_ranking_cfg:
        alt_solver_url = post_construction_ranking_cfg["solver_url"]
    else:
        alt_solver_url = None
    seed = general_cfg['seed']
    model_name = setup_sentence_encoder_cfg['model_name']
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
        raise ValueError("best_model_path is None")

    loading_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/02_intermediate/action_schema_combination')
    loading_data_subdirs = glob(os.path.join(loading_data_dir, '*'))

    # sample dirname "libraryworld_detailed_ensemble_10_use_cp_True_alpha_0.1" | "libraryworld_detailed_ensemble_10_use_cp_False"

    for loading_data_subdir in loading_data_subdirs:
        subdir_basename = os.path.basename(loading_data_subdir)
        # parse the subdir_basename to get domain_name, description_granularity, ensemble_size, use_cp, alpha
        pattern = re.compile(r'^(?P<domain_name>\w+)_(?P<description_granularity>\w+)_ensemble_(?P<ensemble_size>\d+)_use_cp_(?P<use_cp>\w+)(_alpha_(?P<alpha>[\d.]+))?$')
        match = pattern.match(subdir_basename)
        if match is None:
            raise ValueError(f"subdir_basename {subdir_basename} does not match the pattern")
        domain_name = match.group('domain_name')
        description_granularity = match.group('description_granularity')
        ensemble_size = int(match.group('ensemble_size'))
        use_cp = bool(match.group('use_cp'))
        alpha = match.group('alpha') 
        if alpha is not None:
            alpha = float(alpha)

        # get the valid domains
        valid_domain_files = glob(os.path.join(loading_data_subdir, "domain_model_*.pddl"))
        # TODO debug only take 20
        valid_domain_files = valid_domain_files[:20]
        # get the problem
        problem_file = glob(os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/*/{domain_name}/p*.pddl'))[0]
        problem_basename = os.path.basename(problem_file)
        problem_id_pattern = re.compile(r'p(?P<problem_id>\d+).pddl')
        problem_id_match = problem_id_pattern.match(problem_basename)
        problem_id = int(problem_id_match.group('problem_id'))
        
        # save dir 
        basename = f"{domain_name}_{description_granularity}_ensemble_{ensemble_size}_use_cp_{use_cp}"
        if use_cp:
            basename += f"_alpha_{alpha}"
            
        save_path = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output/llm_to_domain_to_plans', basename, f"summary_for_problem_{problem_id}.jsonl")
        Path(os.path.dirname(save_path)).mkdir(parents=True, exist_ok=True)
        
        with open(problem_file, 'r') as f:
            problem_str = f.read()

        # get action_to_query_dict
        action_to_query_dict = get_llm_input_dict(
            query_domain_name=domain_name,
            desc_granularity=description_granularity,
            if_cot_in_fewshot=False,
        )
        output_jsonl_lst = []
        tqdm_desc = basename
        chunk_size = 20 
        
        for idx in tqdm(range(0, len(valid_domain_files), chunk_size), desc=tqdm_desc):
            query_str_lst = [] 
            action_str_lst = [] 
            valid_domain_files_chunk = valid_domain_files[idx:idx+chunk_size]
            true_chunk_size = len(valid_domain_files_chunk)
            
            for valid_domain_fp in valid_domain_files_chunk:
                with open(valid_domain_fp, 'r') as f:
                    domain_str = f.read()
                domain_model:Domain = DomainParser()(domain_str)
                action_lst = list(domain_model.actions)
                for action in action_lst:
                    query_str_for_embeds = SIMPLER_PROMPT_CONTEXT + action_to_query_dict[action.name]['query']
                    action_str_for_embeds = get_action_schema_answer_str(action)
                    query_str_lst.append(query_str_for_embeds)
                    action_str_lst.append(action_str_for_embeds)
                    
                # get the plan
                call_planer_kwargs = dict(
                    domain_fp_str=domain_str,
                    problem_fp_str=problem_str,
                )
                if alt_solver_url is not None:
                    call_planer_kwargs['solver_url'] = alt_solver_url
                planner_result = call_pddl_planner(
                    **call_planer_kwargs
                )
                assert planner_result['is_ok']
                plan_lst = planner_result['plan_lst']
                output_jsonl_lst.append({
                    "plan": plan_lst,
                    "heuristic": None,
                    "domain_fp": valid_domain_fp,
                })
                
            # get the embeddings
            with torch.no_grad():
                query_embeddings = sentence_model.encode(query_str_lst, convert_to_tensor=True)
                action_embeddings = sentence_model.encode(action_str_lst, convert_to_tensor=True)
                # get the scores, which is the mean of cosine similarity
                scores = F.cosine_similarity(query_embeddings, action_embeddings)
                # reshape the scores
                scores = scores.reshape(true_chunk_size, -1).mean(dim=1).detach().cpu().numpy().tolist()
                assert len(scores) == true_chunk_size
                
            for i, output_json in enumerate(output_jsonl_lst[-true_chunk_size:]):
                output_json['heuristic'] = scores[i]
            
        # sort the output_jsonl_lst by heuristic
        output_jsonl_lst = remove_duplicates_with_weighted_heuristic(output_jsonl_lst)
        # save the output_jsonl_lst
        with open(save_path, 'w') as f:
            for output_json in output_jsonl_lst:
                f.write(json.dumps(output_json) + '\n')
        
            
            
def remove_duplicates_with_weighted_heuristic(output_jsonl_lst):
    # Create a dictionary to store unique items and their occurrences
    unique_items = dict()

    # Group items by their unique identifier (assuming there's a unique field like 'id')
    for item in output_jsonl_lst:
        # Replace 'id' with the actual unique identifier field in your data
        plan_str = str(item['plan'])
        if plan_str not in unique_items:
            unique_items[plan_str] = [[], [], [[-999, None], [-999, None], [-999, None]]] # heuristic, domain_fp, top 3 heuristics and domain_fp
        unique_items[plan_str][0].append(item['heuristic'])
        unique_items[plan_str][1].append(item['domain_fp'])
        for i in range(3):
            if item['heuristic'] > unique_items[plan_str][2][i][0]:
                unique_items[plan_str][2].insert(i, [item['heuristic'], item['domain_fp']])
                unique_items[plan_str][2].pop()
                break
            
    # Function to calculate weighted heuristic
    def calculate_weighted_heuristic(heuristics):
        count = len(heuristics)
        if count == 1:
            return heuristics[0]
        
        # Calculate the mean
        mean_heuristic = sum(heuristics) / count
        
        # Apply a weight based on the count of duplicates
        weight = min(1 + (count - 1) * 0.1, 1.5)  # Cap the weight at 1.5
        
        return mean_heuristic * weight

    # Create the new list with unique items and updated heuristics
    result = []
    for unique_id, val in unique_items.items():
        # Find the original item (we'll use the first occurrence)
        updated_dict = dict()
        updated_dict['plan'] = eval(unique_id)
        updated_dict['heuristic'] = calculate_weighted_heuristic(val[0])
        best_3_domains = []
        for i in range(3):
            best_3_domains.append(val[2][i][1])
        updated_dict['domain_fp'] = best_3_domains
        result.append(updated_dict)
        

    # Sort the result by the updated heuristic in descending order
    return sorted(result, key=lambda x: x['heuristic'], reverse=True)
