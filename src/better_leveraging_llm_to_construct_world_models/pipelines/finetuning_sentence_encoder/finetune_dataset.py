import os
from datasets import Dataset, IterableDataset # iterable dataset allow randomness sampling while Dataset will save cache to disk and any random sampling will be deterministic
# ref: https://discuss.huggingface.co/t/dataset-from-generator-prevent-caching-during-upload/86617/2

import torch
import random
from copy import deepcopy
import json
import random
from typing import Sequence
from tqdm.auto import tqdm
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import numpy as np 
from pathlib import Path
import os 
from glob import glob 
from pddl.parser.domain import DomainParser
from enum import Enum
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect
from datasets import load_dataset

from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str
import json 

class TorchDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        negative_weights,
        dir_path,
        expand_size = False,
        estimate_batch_size = 32,
    ):
        self.negative_weights = negative_weights # control the probability of sampling easy / semi-hard / hard negatives
        self.estimate_batch_size = estimate_batch_size
        self.expand_size = expand_size
        
        domain_filepaths = glob(os.path.join(dir_path, f"**/domain_groundtruth.pddl"), recursive=True)
        self.data = pd.DataFrame(columns=["domain_name", 'action_model', 'action_name', 'query_content', "positive_answer_content", "desc_granularity"])
        self.manipulated_action_models_dict = dict() # key is f'{domain_name}_{action_name}', val is list of manipulated action models
        for domain_filepath in tqdm(domain_filepaths, desc="Setting up dataset"):
            domain_name = os.path.basename(os.path.dirname(domain_filepath))
            with open(domain_filepath, 'r') as f:
                domain_str = f.read()
            domain_model = DomainParser()(domain_str)
            action_model_list = list(domain_model.actions)
            action_to_query_dict_detailed = get_llm_input_dict(
                query_domain_name = domain_name,
                desc_granularity = "detailed",
                if_cot_in_fewshot = False,
            )
            action_to_query_dict_layman  = get_llm_input_dict(
                query_domain_name = domain_name,
                desc_granularity = "layman",
                if_cot_in_fewshot = False,
            )
            for action_model in tqdm(action_model_list, desc=f"Setting up dataset for {domain_name}", leave=False):
                action_name = action_model.name
                # get the manipulated action models
                manipulated_action_lst, _ = get_manipulated_action_lst(action_model, self.estimate_batch_size)
                self.manipulated_action_models_dict[f"{domain_name}_{action_name}"] = manipulated_action_lst
                # get the query content
                query_content_detailed = action_to_query_dict_detailed[action_name]['query']
                query_content_layman = action_to_query_dict_layman[action_name]['query']
                # get the positive answer content
                positive_answer_content = get_action_schema_answer_str(action_model)
                # add two rows, one for detailed, one for layman
                self.data.loc[len(self.data)] = {
                    "domain_name": domain_name,
                    'action_model': action_model,
                    'action_name': action_name,
                    'query_content': SIMPLER_PROMPT_CONTEXT + query_content_detailed,
                    "positive_answer_content": positive_answer_content,
                    "desc_granularity": "detailed",
                }
                self.data.loc[len(self.data)] = {
                    "domain_name": domain_name,
                    'action_model': action_model,
                    'action_name': action_name,
                    'query_content': SIMPLER_PROMPT_CONTEXT + query_content_layman,
                    "positive_answer_content": positive_answer_content,
                    "desc_granularity": "layman",
                }

    def __len__(self):
        if self.expand_size:
            return len(self.data) * 50
        else:
            return len(self.data)

    def __getitem__(self, idx):
        idx = idx % len(self.data)
        # first determine the negative example type by sampling from the negative_weights
        idx_domain_name = self.data.iloc[idx]["domain_name"]
        idx_action_name = self.data.iloc[idx]["action_name"]
        output_dict = {
            "anchor": self.data.iloc[idx]["query_content"],
            "positive": self.data.iloc[idx]["positive_answer_content"],
        }
        negative_example_type = random.choices(["easy", "semi-hard", "hard"], weights=self.negative_weights, k=1)[0]
        if negative_example_type == "easy":
            # select a action model that is not from the same domain 
            want_ids =  np.where(self.data["domain_name"] != idx_domain_name)
            # randomly select a row
            selected_row = self.data.iloc[random.choice(want_ids[0])]
            output_dict["negative"] = selected_row["positive_answer_content"]
             
        elif negative_example_type == "semi-hard":
            # select a action model that is from the same domain but not the same action name 
            cond1 = self.data["domain_name"] == idx_domain_name
            cond2 = self.data["action_name"] != idx_action_name
            want_ids = np.where(cond1 & cond2)
            # randomly select a row
            selected_row = self.data.iloc[random.choice(want_ids[0])]
            output_dict["negative"] = selected_row["positive_answer_content"]
        elif negative_example_type == "hard":
            # select a manipulated action model
            manipulated_action_lst = self.manipulated_action_models_dict[f"{idx_domain_name}_{idx_action_name}"]
            # randomly pick a index 
            selected_idx = random.choice(range(len(manipulated_action_lst)))
            selected_manipulated_action = manipulated_action_lst[selected_idx]
            output_dict["negative"] = get_action_schema_answer_str(selected_manipulated_action)
            # pop that action model from the list
            self.manipulated_action_models_dict[f"{idx_domain_name}_{idx_action_name}"].pop(selected_idx)
            # if the list is empty, then regenerate the list
            if len(self.manipulated_action_models_dict[f"{idx_domain_name}_{idx_action_name}"]) == 0:
                self.manipulated_action_models_dict[f"{idx_domain_name}_{idx_action_name}"] = get_manipulated_action_lst(self.data.iloc[idx]['action_model'], self.estimate_batch_size)[0]
        return output_dict
    
    def shuffle(self):
        self.data = self.data.sample(frac=1).reset_index(drop=True)
                

class TorchTestDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        dataframe,
    ):
        self.data = dataframe
        # only keep Comparison Mode ==  'NL Desc vs. Action Schema'
        self.data = self.data[self.data['Comparison Mode'] == 'NL Desc vs. Action Schema']
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        # return the dict type of data
        return self.data.iloc[idx].to_dict()



def create_train_dataset():
    data_dir = os.path.join(os.environ['WORKING_DIR'], "data/02_intermediate/pddl_domain/train_dataset")
    data_paths = glob(os.path.join(data_dir, "*.jsonl"))
    # train_dataset = load_dataset("json", data_files=data_paths, split="train", streaming=True)
    train_dataset = load_dataset("json", data_files=data_paths, split="train")
    print("Length of train dataset: ", len(train_dataset))
    return train_dataset
    

def create_eval_dataset():
    data_dir = os.path.join(os.environ['WORKING_DIR'], "data/02_intermediate/pddl_domain/eval_dataset")
    data_path = os.path.join(data_dir, "eval_data.jsonl")
    eval_dataset = load_dataset("json", data_files=data_path, split="train")
    print("Length of eval dataset: ", len(eval_dataset))
    return eval_dataset
    

def create_test_dataset(cosine_sim_comparison_data):
    test_dataset = TorchTestDataset(cosine_sim_comparison_data)
    print("Length of test dataset: ", len(test_dataset))
    return test_dataset 


def generate_training_dataset(train_negative_weights, total_num_examples = 2.0e5, chunksize=10000):
    data_dir = os.path.join(os.environ['WORKING_DIR'], "data/01_raw/pddl_domain/validation_set")
    train_dataset = TorchDataset(negative_weights=train_negative_weights, dir_path=data_dir) 
    save_dir = os.path.join(os.environ['WORKING_DIR'], "data/02_intermediate/pddl_domain/train_dataset")
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    file_id = 0 
    num_count = 0 
    output_lst = [] 
    pbar = tqdm(total=total_num_examples, desc="Generating training dataset")
    while num_count < total_num_examples:
        for i in range(len(train_dataset)):
            output_lst.append(json.dumps(train_dataset[i]))
            num_count += 1
            pbar.update(1)
            if len(output_lst) == chunksize:
                # save jsonl file 
                with open(os.path.join(save_dir, f"train_data_{file_id}.jsonl"), 'w') as f:
                    f.write("\n".join(output_lst))
                file_id += 1
                output_lst = []
        # shuffle the dataset after each epoch
        train_dataset.shuffle()
    # save the last chunk
    with open(os.path.join(save_dir, f"train_data_{file_id}.jsonl"), 'w') as f:
        f.write("\n".join(output_lst))
    pbar.close()
    
    

def generate_eval_dataset(eval_negative_weights):
    data_dir = os.path.join(os.environ['WORKING_DIR'], "data/01_raw/pddl_domain/testing_set") 
    eval_dataset = TorchDataset(negative_weights=eval_negative_weights, dir_path=data_dir)
    save_dir = os.path.join(os.environ['WORKING_DIR'], "data/02_intermediate/pddl_domain/eval_dataset")
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    output_lst = [] 
    for i in tqdm(range(len(eval_dataset))):
        output_lst.append(json.dumps(eval_dataset[i]))
        
    # save into one jsonl file
    with open(os.path.join(save_dir, "eval_data.jsonl"), 'w') as f:
        f.write("\n".join(output_lst))
        
        
    
    

if __name__ == "__main__":
    generate_training_dataset([0.0, 0.4, 0.6])
    generate_eval_dataset([0.0, 0.3, 0.7])
    # train_dataset = create_train_dataset()
    # eval_dataset = create_eval_dataset()
            

