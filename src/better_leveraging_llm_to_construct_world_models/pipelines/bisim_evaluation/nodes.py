"""
This is a boilerplate pipeline 'bisim_evaluation'
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

from better_leveraging_llm_to_construct_world_models.pipelines.bisim_evaluation.grade import format_results, grade
from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner

# ! NODE 
def bisim_evaluate(bisim_evaluation_cfg):
    top_k = bisim_evaluation_cfg['top_k']
    val_path = bisim_evaluation_cfg['val_path']
    ensemble_size = bisim_evaluation_cfg['ensemble_size']
    cp_alpha = bisim_evaluation_cfg['cp_alpha']
    
    testing_domain_dirs = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain/testing_set')
    
    testing_domain_dirs = glob(testing_domain_dirs + '/*')
    domain_names = [os.path.basename(domain_dir) for domain_dir in testing_domain_dirs]
    
    plan_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output/llm_to_domain_to_plans')
    
    desc_granularity_lst = ['detailed', 'layman']
    
    total_results = {}
    
    for domain_ind, domain_name in enumerate(domain_names):
        
        reference_domain_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/domain_groundtruth.pddl')
        problem_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/p0.pddl')
        for desc_gran in desc_granularity_lst:
            # example: libraryworld_detailed_ensemble_15_use_cp_True_alpha_0.2
            basename = f"{domain_name}_{desc_gran}_ensemble_{ensemble_size}_use_cp_True_alpha_{cp_alpha}"
            plan_path = os.path.join(plan_data_dir, basename, "summary_for_problem_0.jsonl")
            plan_data_lst = [] 
            with open(plan_path, 'r') as f:
                for line in f:
                    plan_data_lst.append(json.loads(line))
                    
            # already sorted, now get top k 
            top_k_plan_data_lst = plan_data_lst[:top_k]
            # now get all the domain files 
            submission_domain_fp_lst = [] 
            for plan_data in top_k_plan_data_lst:
                submission_domain_fp_lst.extend(plan_data['domain_fp'])
                
            # remove the old marking folder
            marking_dir_path = os.path.join(Path(__file__).parent.resolve(), "marking", domain_name)
            marking_merge_dir_path = os.path.join(Path(__file__).parent.resolve(), "merge", domain_name)
            submission_dir_path = os.path.join(Path(__file__).parent.resolve(), "submission", domain_name)
            reference_dir_path = os.path.join(Path(__file__).parent.resolve(), "reference", domain_name)

            working_dir = os.path.join(Path(__file__).parent.resolve())
            os.chdir(working_dir)
            
            # delete the old marking folder 
            if os.path.exists(marking_dir_path):
                os.system(f'rm -rf {marking_dir_path}')
                os.system(f'rm -rf {marking_merge_dir_path}')
                os.system(f'rm -rf {submission_dir_path}')
                os.system(f'rm -rf {reference_dir_path}')
                
            for ind, submission_domain_fp in enumerate(submission_domain_fp_lst):
                print(f"-- {ind+1}/{len(submission_domain_fp_lst)} --")
                try:
                    res = grade(domain_name, reference_domain_fp, submission_domain_fp, problem_fp, submission_id=str(ind))
                    # update name 
                    assert len(res) == 1
                    new_res = dict()
                    for k in res:
                        new_res[k+f"_submission_{ind}_{desc_gran}"] = res[k]
                        new_res[k+f"_submission_{ind}_{desc_gran}"]['Domain-Name'] = k
                        new_res[k+f"_submission_{ind}_{desc_gran}"]['Desc-Granularity'] = desc_gran
                    res = new_res
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                # update result 
                total_results.update(res)
                
    # format results
    res = format_results(total_results)
    # write to file
    grade_txt_fp = os.path.join(os.path.join(os.path.dirname(__file__)), "marking", "all_grade.txt")
    # create the parent dir 
    Path(os.path.dirname(grade_txt_fp)).mkdir(parents=True, exist_ok=True)
    # need to add explanation for each column
    exp_str = """Explanation:
Solve: This term is used to assess whether the planner can find a plan based on the generated domain model.
St-Validates: This term is used to assess whether the plan generated from the domain model is valid when applied to the actual groundtruth domain setting.
Ref-Validates: This term is used to evaluate whether the reference solution (groundtruth plan) is valid when applied to the generated domain model.
Aligns: This term is used to assess the equivalence between two planning domains are “equivalent” using Bisimulation theory."""
    with open(grade_txt_fp, 'w', encoding='utf-8') as f:
        f.write(f'\n{exp_str}\n\n')
        f.write(f'#\n{res}\n\n')
        
    # also convert to dataframe and save to csv
    df  = pd.DataFrame(total_results)
    df.to_csv(grade_txt_fp.replace('.txt', '.csv'))
    print('Done!\n')
    
    return df 
    




