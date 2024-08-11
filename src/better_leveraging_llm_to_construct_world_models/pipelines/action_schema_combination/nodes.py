"""
This is a boilerplate pipeline 'action_schema_combination'
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


from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str
from natsort import natsorted

# ! NODE 
def action_schema_combi(general_cfg, setup_sentence_encoder_cfg, finetuning_encoder_cfg, action_schema_combination_cfg, cp_threshold_json):
    seed = general_cfg['seed']
    use_cp_filtering = action_schema_combination_cfg['use_cp_filtering']
    cp_alpha_lst = action_schema_combination_cfg['cp_alpha_lst']
    if use_cp_filtering:
        ensemble_size_lst = action_schema_combination_cfg['use_cp_params']['ensemble_size_lst']
    else:
        ensemble_size_lst = action_schema_combination_cfg['no_cp_params']['ensemble_size_lst']
   
    cp_threshold_lst = [] 
    for cp_alpha in cp_alpha_lst:
        corresponding_dict = [d for d in cp_threshold_json if d['alpha'] == cp_alpha][0]
        cp_threshold_lst.append(corresponding_dict['threshold_val'])

    desc_granularity_lst = ['detailed', 'layman']

    # setup sentence encoder
    if use_cp_filtering:
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
            raise ValueError('best_model_path is None')

    testing_domain_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain/testing_set')

    analysis_dataframe = pd.DataFrame(columns=['Domain Name', 'Desc Granularity', 'Ensemble Size', 'Total Combinations', 'Valid Combinations', "Applied CP Threshold", "CP Threshold Value"])

    testing_domain_dirs = glob(testing_domain_data_dir + '/*')
    for testing_domain_dir in testing_domain_dirs:
        testing_domain_name = testing_domain_dir.split('/')[-1]
        action_lst_datapath = os.path.join(testing_domain_dir, 'action_name_lst.json')
        with open(action_lst_datapath, 'r') as f:
            action_name_lst = json.load(f)

        # load problem file
        problem_file_path = os.path.join(testing_domain_dir, 'p0.pddl')
        with open(problem_file_path, 'r') as f:
            problem_str = f.read()

        domain_requirement_module = None 
        domain_types_module = None
        domain_constants_module = None
        domain_predicates_module = None
        domain_derived_predicates_module = None

        for desc_granularity in desc_granularity_lst:
            action_to_query_dict = get_llm_input_dict(
                query_domain_name = testing_domain_name,
                desc_granularity = desc_granularity,
                if_cot_in_fewshot = False,
            )

            # get post_generate_schema_pool generated pddl models
            post_generate_schema_pool_generated_pddl_models_dir = os.path.join(os.environ['WORKING_DIR'], f'data/02_intermediate/post_generate_schema_pool/{testing_domain_name}_{desc_granularity}_cot_True')

            raw_generated_domain_files = glob(os.path.join(post_generate_schema_pool_generated_pddl_models_dir, "**/generated_domain_id_*.pddl"), recursive=True)
            raw_generated_domain_files = natsorted(raw_generated_domain_files)
            # set seed
            random.seed(seed)
            np.random.seed(seed)
            for ensemble_size in ensemble_size_lst:
                # randomly select ensemble_size number of pddl models
                selected_pddl_models = random.sample(raw_generated_domain_files, ensemble_size)
                selected_pddl_models = natsorted(selected_pddl_models)

                if use_cp_filtering:
                    iteration_lst = cp_threshold_lst
                else:
                    iteration_lst = [None]

                for cp_indx, cp_threshold in enumerate(iteration_lst):
                    # get action schema from selected pddl models
                    action_schema_lst_dict = dict()
                    for action_name in action_name_lst:
                        action_schema_lst_dict[action_name] = set()

                    max_score_action_dict = dict() 
                    max_score_dict = dict()
                    for action_name in action_name_lst:
                        max_score_action_dict[action_name] = None
                        max_score_dict[action_name] = -9999
                    
                    for pddl_model_fp in selected_pddl_models:
                        with open(pddl_model_fp, 'r') as f:
                            pddl_model_str = f.read()
                        domain_model:Domain = DomainParser()(pddl_model_str)
                        if domain_requirement_module is None:
                            domain_requirement_module = domain_model.requirements
                            domain_types_module = domain_model.types
                            domain_constants_module = domain_model.constants
                            domain_predicates_module = domain_model.predicates
                            domain_derived_predicates_module = domain_model.derived_predicates
                        actions = list(domain_model.actions)
                        if cp_threshold is None:
                            for action in actions:
                                action_name = action.name
                                action_schema_lst_dict[action_name].add(action)
                        else:
                            # ! filter action schema based on semantic validator cosine sim score
                            query_lst = [] 
                            action_lst = []
                            for action in actions:
                                action_name = action.name
                                query_content_temp_dict = action_to_query_dict[action_name] 
                                query_str_for_embeds = SIMPLER_PROMPT_CONTEXT + query_content_temp_dict['query']
                                action_str_for_embeds = get_action_schema_answer_str(action)
                                query_lst.append(query_str_for_embeds)
                                action_lst.append(action_str_for_embeds)
                            with torch.no_grad():
                                query_embeds = sentence_model.encode(query_lst, convert_to_tensor=True)
                                action_embeds = sentence_model.encode(action_lst, convert_to_tensor=True)
                                cosine_sim_score = F.cosine_similarity(query_embeds, action_embeds).detach().cpu().numpy().tolist()
                            
                            
                            for action_i, action in enumerate(actions):
                                if cosine_sim_score[action_i] > max_score_dict[action.name]:
                                    max_score_dict[action.name] = cosine_sim_score[action_i]
                                    max_score_action_dict[action.name] = action
                                    
                                if cosine_sim_score[action_i] >= cp_threshold:
                                    action_name = action.name
                                    action_schema_lst_dict[action_name].add(action)
                    
                    # if we see not actions are selected, then we will select the action with highest cosine sim score
                    for action_name in action_name_lst:
                        if len(action_schema_lst_dict[action_name]) == 0:
                            action_schema_lst_dict[action_name].add(max_score_action_dict[action_name])
                            

                    # get action schema combination
                    # first of all, calculate the total number of possible combinations
                    total_combinations = 1
                    for action_name in action_name_lst:
                        total_combinations *= len(action_schema_lst_dict[action_name])

                    # get all possible combinations
                    all_combinations = list(itertools.product(*[action_schema_lst_dict[action_name] for action_name in action_name_lst]))
                    assert len(all_combinations) == total_combinations

                    args = [] 
                    ensemble_domain_model_lst = [] 
                    manager = Manager()
                    plan_valid_id_lst = manager.list()

                    get_ensemble_domain_args = [] 
                    if use_cp_filtering:
                        tqdm_desc = f"Domain: {testing_domain_name}, Gran: {desc_granularity}, Ensemble Size: {ensemble_size}, CP_alpha: {cp_alpha_lst[cp_indx]}"
                    else:
                        tqdm_desc = f"Domain: {testing_domain_name}, Gran: {desc_granularity}, Ensemble Size: {ensemble_size} No CP"
                    for action_combi_i, action_combi in enumerate(tqdm(all_combinations, desc=tqdm_desc)):
                        get_ensemble_domain_args.append((testing_domain_name, domain_requirement_module, domain_types_module, domain_constants_module, domain_predicates_module, domain_derived_predicates_module, action_combi))
                        
                    with Pool(8) as p:
                        domain_n_str_zip_lst = list(tqdm(p.imap(mp_helper_func_for_get_ensemble_domain_model, get_ensemble_domain_args, chunksize=10), total=len(get_ensemble_domain_args), desc="Getting Ensemble Domain Models"))
                    
                    for idx, (domain_m, domain_str) in enumerate(domain_n_str_zip_lst):
                        ensemble_domain_model_lst.append(domain_m)
                        args.append((idx, domain_str, problem_str, plan_valid_id_lst))

                    # send to external planner
                    with Pool(16) as p:
                        temp = list(tqdm(p.imap(mp_helper_func_for_check_plan_valid, args, chunksize=1), total=len(args), desc="Calling Planner"))

                    plan_valid_id_lst = list(plan_valid_id_lst)
                    plan_valid_id_lst = sorted(plan_valid_id_lst)
                    # store the domain model
                    temp_save_str = f'data/02_intermediate/action_schema_combination/{testing_domain_name}_{desc_granularity}_ensemble_{ensemble_size}_use_cp_{use_cp_filtering}'
                    if use_cp_filtering:
                        temp_save_str += f'_alpha_{cp_alpha_lst[cp_indx]}'
                    domain_model_dir = os.path.join(os.environ['WORKING_DIR'], temp_save_str)
                    Path(domain_model_dir).mkdir(parents=True, exist_ok=True)
                    for action_combi_i in plan_valid_id_lst:
                        domain_model_fp = os.path.join(domain_model_dir, f'domain_model_{action_combi_i}.pddl')
                        with open(domain_model_fp, 'w') as f:
                            f.write(domain_to_string(ensemble_domain_model_lst[action_combi_i]))

                    # update the dataframe
                    update_info_dict = {
                        'Domain Name': testing_domain_name,
                        'Desc Granularity': desc_granularity,
                        'Ensemble Size': ensemble_size,
                        'Total Combinations': total_combinations,
                        'Valid Combinations': len(plan_valid_id_lst),
                        "Applied CP Threshold": use_cp_filtering,
                        "CP Threshold Value": cp_threshold,
                    }

                    analysis_dataframe.loc[len(analysis_dataframe)] = update_info_dict

    return analysis_dataframe 


def get_ensemble_domain_model(
    testing_domain_name,
    domain_requirement_module,
    domain_types_module,
    domain_constants_module,
    domain_predicates_module,
    domain_derived_predicates_module,
    action_combi,
):
    ensemble_domain_model = Domain(
        name=testing_domain_name,
        requirements=domain_requirement_module,
        types=domain_types_module,
        constants=domain_constants_module,
        predicates=domain_predicates_module,
        derived_predicates=domain_derived_predicates_module,
        actions=action_combi,
    )
    # make it str
    domain_str = domain_to_string(ensemble_domain_model)
    return ensemble_domain_model, domain_str

def mp_helper_func_for_get_ensemble_domain_model(args):
    return get_ensemble_domain_model(*args)


def mp_helper_func_for_check_plan_valid(args):
    return call_planner_and_find_valid(*args) 

def call_planner_and_find_valid(domain_id, domain_str, problem_str, plan_valid_id_lst):
    try_limit = 3 
    for i in range(try_limit):
        planner_result = call_pddl_planner(domain_str, problem_str)
        if planner_result is None:
            continue
        else:
            if planner_result['is_ok']:
                plan_valid_id_lst.append(domain_id)
                return True 
            else:
                return False 
    return False

