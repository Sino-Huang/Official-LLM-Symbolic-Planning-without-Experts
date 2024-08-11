"""
This is a boilerplate pipeline 'plan_evaluation'
generated using Kedro 0.19.6
"""
import logging
from pathlib import Path

# utils
import os
import json
from copy import deepcopy
from functools import cache
import random
from glob import glob
import re
import numpy as np
import pandas as pd
from pddl.formatter import domain_to_string, problem_to_string
from natsort import natsorted
import wandb
import subprocess
from tabulate import tabulate



# combination utils
from itertools import product

# PDDL utils
from pddl.parser.domain import DomainParser
from pddl.parser.problem import ProblemParser, ProblemTransformer
from pddl.helpers.base import _typed_parameters
from pddl.logic.predicates import Predicate
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.logic.effects import AndEffect


# multiprocessing
from multiprocessing import Pool
from multiprocess.dummy import Pool as DummyPool
from tqdm.auto import tqdm

# icecream
from icecream import ic

from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath

# ! NODE 
def human_plan_eval(plan_evaluation_cfg):
    top_k = plan_evaluation_cfg['top_k']
    ensemble_size = plan_evaluation_cfg['ensemble_size']
    cp_alpha = plan_evaluation_cfg['cp_alpha']
    
    analysis_df = pd.DataFrame(columns=[
        'Domain',
        'Problem Desc',
        "Desc Granularity",
        'Plan',
        "Plan Type", # "gold", "tot_direct_planning", "pddl_to_plan"
        "Human Rating",
    ])
    
    testing_domain_dirs = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain/testing_set')
    
    testing_domain_dirs = glob(testing_domain_dirs + '/*')
    domain_names = [os.path.basename(domain_dir) for domain_dir in testing_domain_dirs]
    desc_granularity_lst = ['detailed', 'layman']
    
    
    
    pddl_to_plan_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output/llm_to_domain_to_plans')
    tot_direct_plan_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output/tree_of_thought_plans')
    
    for domain_name in domain_names:
        # get gold plan 
        reference_domain_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/domain_groundtruth.pddl')
        problem_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/p0.pddl')
        gold_plan = call_pddl_planner(reference_domain_fp, problem_fp)['plan_lst']
        
        # get problem desc
        problem_info_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/problem_info.py')
        domain_info_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/data.py')
        problem_info = import_from_filepath(problem_info_fp)
        problem_desc = f"""Problem Object Desc:
{problem_info.OBJECT_SNIPPET_STR}

Problem Init State Desc:
{problem_info.INIT_STATE_DESC}

Problem Goal State Desc:
{problem_info.GOAL_STATE_DESC}

"""


        domain_info = import_from_filepath(domain_info_fp)
        domain_nl_desc = domain_info.DOMAIN_DESC
        domain_predicate_desc = "\n".join(
        [f"{i+1}. {predicate}" for i, predicate in enumerate(domain_info.PREDICATE_DESC_LST)]
    )
        
        for desc_granularity in desc_granularity_lst:
            action_nl_desc = ""
            for action_name, action_info in domain_info.ACTION_DESC_DICT.items():
                action_nl_desc += (
                    f"Action Name: {action_name}\n"
                    f"Action Desc: {action_info[desc_granularity]}\n\n" 
                )
            
            
            
            tag_name = f"{domain_name}_{desc_granularity}_ensemble_{ensemble_size}_use_cp_True_alpha_{cp_alpha}"
            pddl_to_plan_data_path = os.path.join(pddl_to_plan_data_dir, tag_name, "summary_for_problem_0.jsonl")
            assert os.path.exists(pddl_to_plan_data_path), f"{pddl_to_plan_data_path} does not exist"
            
            tag_name = f"{domain_name}_{desc_granularity}"
            tot_direct_plan_data_path = os.path.join(tot_direct_plan_data_dir, tag_name, "glm-4*/**/summary_for_problem_0.jsonl")
            tot_direct_plan_data_path = glob(tot_direct_plan_data_path, recursive=True)[0]
            assert os.path.exists(tot_direct_plan_data_path), f"{tot_direct_plan_data_path} does not exist"
            
            # load pddl_to_plan data
            pddl_to_plan_lst = []
            with open(pddl_to_plan_data_path, 'r') as f:
                for line in f:
                    pddl_to_plan_lst.append(json.loads(line))
                    
            # load tot_direct_plan data
            tot_direct_plan_lst = []
            with open(tot_direct_plan_data_path, 'r') as f:
                for line in f:
                    tot_direct_plan_lst.append(json.loads(line))
                    
            # remove duplicates 
            unique_pddl_to_plan_set = set()
            unique_pddl_to_plan_lst = [] 
            for plan_data in pddl_to_plan_lst:
                if str(plan_data['plan']) not in unique_pddl_to_plan_set:
                    unique_pddl_to_plan_lst.append(plan_data)
                unique_pddl_to_plan_set.add(str(plan_data['plan']))
                
                
            unique_tot_direct_plan_set = set()
            unique_tot_direct_plan_lst = [] 
            for plan_data in tot_direct_plan_lst:
                if str(plan_data['plan']) not in unique_tot_direct_plan_set:
                    unique_tot_direct_plan_lst.append(plan_data)
                unique_tot_direct_plan_set.add(str(plan_data['plan']))
            
                    
            # get top k
            pddl_to_plan_lst = pddl_to_plan_lst[:top_k]
            tot_direct_plan_lst = tot_direct_plan_lst[:top_k]
            
            # check if some plan is less than top k, then duplicate the last plan
            while len(pddl_to_plan_lst) < top_k:
                pddl_to_plan_lst.append(deepcopy(pddl_to_plan_lst[-1]))
                
            while len(tot_direct_plan_lst) < top_k:
                tot_direct_plan_lst.append(deepcopy(tot_direct_plan_lst[-1]))
                
            camera_plan_lst = [str(gold_plan)+"_"] + [plan_data['plan'] for plan_data in pddl_to_plan_lst] + [plan_data['plan'] for plan_data in tot_direct_plan_lst]
            camera_plan_type_lst = ["Gold"] + ["PDDL to Plan"]*top_k + ["Tot Direct Plan"]*top_k
            
            # random the index 
            rand_idx = np.random.permutation(len(camera_plan_lst))
            
            camera_plan_lst = [camera_plan_lst[idx] for idx in rand_idx]
            camera_plan_type_lst = [camera_plan_type_lst[idx] for idx in rand_idx]
            
            # setup query str, give domain desc, action desc and problem desc 
            # TODO 
            query_str = (
                f"\n\n\n\n\n"
                f"Action Desc: {action_nl_desc}\n"
                f"Domain Predicate Desc: {domain_predicate_desc}\n\n"
                f"Domain Name: {domain_name}\n"
                f"Domain NL Desc: {domain_nl_desc}\n"
                f"Problem Desc: {problem_desc}\n"
            )
            query_str += "Please rank the following plans, output format should be comma separated, e.g. 3,1,2,5,4, which means 3rd plan is the best, 1st plan is the second best, and so on. \n\n"
            for i, plan in enumerate(camera_plan_lst):
                query_str += f"{i+1}. {plan}\n"
                
            # get human rating
            human_rating_order = input(query_str)
            # parse it 
            human_rating_order = human_rating_order.split(",")
            human_rating_order = [int(rating) -1 for rating in human_rating_order]
            rank = list(range(1, len(camera_plan_lst)+1))
            human_rating = [] 
            for i in range(len(camera_plan_lst)):
                human_rating.append(rank[human_rating_order.index(i)])
            
                
            
            # update analysis_df
            update_dict = {
                'Domain': domain_name,
                'Problem Desc': problem_desc,
                "Desc Granularity": desc_granularity,
                'Plan': camera_plan_lst,
                "Plan Type": camera_plan_type_lst,
                "Human Rating": human_rating,
            }
            
            analysis_df = pd.concat([analysis_df, pd.DataFrame(update_dict)], ignore_index=True)
            
    return analysis_df

