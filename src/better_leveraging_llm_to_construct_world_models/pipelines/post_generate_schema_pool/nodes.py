"""
This is a boilerplate pipeline 'post_generate_schema_pool'
generated using Kedro 0.19.6
"""
from copy import deepcopy
from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
import os 
from zhipuai import ZhipuAI
import random 
import numpy as np
from icecream import ic
from tqdm.auto import tqdm
import json 
import re 
from glob import glob 
from natsort import natsorted
from pddl.parser.domain import DomainParser

from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath



def parse_single_response_dict_to_action_schema(response_dict):
    assert "action" in response_dict and "type" in response_dict and response_dict["type"] == "response"
    
    action_name = response_dict["action"]
    response_str = response_dict["content"]
    
    parameters_str = f"    :parameters {helper_parse_action_parameters(response_str)}"
    precondition_str = f"    :precondition {helper_parse_action_preconditions(response_str)}"
    effect_str = f"    :effect {helper_parse_action_effects(response_str)}"
    
    output = (
        f"(:action {action_name}\n"
        f"    {parameters_str}\n"
        f"    {precondition_str}\n"
        f"    {effect_str}\n"
        f"    )"
    )
    
    return output
    
    
    
def convert_pddl_domain_snippet_str_from_info(predicate_desc_lst, domain_name, type_info_str, action_snippet_lst):
    requirements_str = "(:requirements :strips :typing :negative-preconditions)"
    predicates_str = "\n".join([f"        {predicate_desc}" for predicate_desc in predicate_desc_lst])
    actions_str = "\n".join(f"    {action_snippet}" for action_snippet in action_snippet_lst)
    
    output_domain_str = (
        f"(define (domain {domain_name})\n\n"
        f"    {requirements_str}\n\n"
        f"    {type_info_str}\n\n"
        f"    (:predicates\n"
        f"{predicates_str}\n"
        f"    )\n\n"
        f"{actions_str}\n"
        f")"
    )
    
    return output_domain_str



# ! NODE
def post_generate_schema_pool_parsing(post_generate_schema_pool_cfg):
    is_generation_complete = post_generate_schema_pool_cfg['is_generation_complete']
    
    if not is_generation_complete:
        dir_path = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output/pure_generate_schema_pool')
        
        # get all the subdirectories
        subdirs = glob(os.path.join(dir_path, "*"))
        for sub_dir in tqdm(subdirs, desc="Working on subdirectories"):
            # get the basename 
            sub_dir_basename = os.path.basename(sub_dir)
            # example "libraryworld_detailed_cot_True"
            # get domain, desc_granularity, if_cot_in_fewshot
            domain_name_gran, if_cot_in_fewshot = sub_dir_basename.split("_cot_")
            # get the domain name and desc_granularity
            *domain_name, desc_granularity = domain_name_gran.split("_")
            domain_name = "_".join(domain_name)
            
            # get the domain info
            domain_info_fp = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain', f"**/{domain_name}", "data.py")
            domain_info_fp = glob(domain_info_fp, recursive=True)[0]
            domain_info_module = import_from_filepath(domain_info_fp)
            predicate_desc_lst = domain_info_module.PREDICATE_DESC_LST
            type_info_str = domain_info_module.TYPE_INFO_STR
            
            print(f"Domain: {domain_name}, Desc Granularity: {desc_granularity}, CoT in Fewshot: {if_cot_in_fewshot}")
            
            # continue get the conversation_id_x.jsonl
            conversation_jsonl_pattern = os.path.join(sub_dir, "*/conversation_id_*.jsonl")
            conversation_jsonl_filepaths = glob(conversation_jsonl_pattern)
            # get model tag 
            model_tag = os.path.basename(os.path.dirname(conversation_jsonl_filepaths[0]))
            print(model_tag)
            
            conversation_jsonl_filepaths = natsorted(conversation_jsonl_filepaths)
            for id, conv_jsonl_fp in enumerate(tqdm(conversation_jsonl_filepaths, desc="convert jsonls", leave=False)):
                response_lst = gather_response_from_jsonl(conv_jsonl_fp)
                # get the domain info
                action_str_lst = [] 
                for response_dict in response_lst:
                    action_str = parse_single_response_dict_to_action_schema(response_dict)
                    action_str_lst.append(action_str)
                    
                # convert to domain string
                domain_str = convert_pddl_domain_snippet_str_from_info(
                    predicate_desc_lst = predicate_desc_lst,
                    domain_name = domain_name,
                    type_info_str = type_info_str,
                    action_snippet_lst = action_str_lst,
                )
                
                # save it 
                save_dir = os.path.join(os.environ['WORKING_DIR'], 'data/02_intermediate/post_generate_schema_pool', f"{domain_name}_{desc_granularity}_cot_{if_cot_in_fewshot}", model_tag)
                Path(save_dir).mkdir(parents=True, exist_ok=True)
                save_fp = os.path.join(save_dir, f"generated_domain_id_{id}.pddl")
                
                with open(save_fp, "w") as f:
                    f.write(domain_str)
                    
    # ! step 2, re parse the domain 
    # get all the subdirectories
    file_paths = glob(os.path.join(os.environ['WORKING_DIR'], 'data/02_intermediate/post_generate_schema_pool', "**/generated_domain_id_*.pddl"), recursive=True)
    error_count = 0
    for file in file_paths:
        with open(file, "r") as f:
            domain_str = f.read()
        try:
            domain_model = DomainParser()(domain_str)
        except Exception as e:
            error_count += 1
            print(f"Error parsing domain: {e}")
            print(f"{error_count}. Please use vscode-pddl extension to rectify syntax error in File: {file}")
    
    return None
            

def gather_response_from_jsonl(jsonl_fp):
    """
    Gather the response from a jsonl file.

    Args:
        jsonl_fp (str): The file path to the jsonl file.

    Returns:
        dict: The response dictionary.
    """
    response_lst = []
    with open(jsonl_fp, "r") as f:
        for line in f:
            line_dict = json.loads(line)
            # only keep dict where has key "type" and the value is response
            if "type" in line_dict and line_dict["type"] == "response":
                response_lst.append(line_dict)
                
    return response_lst



def user_input_func():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError: # press ctrl+d
            break
    response = '\n'.join(lines)
    return response

def helper_parse_action_preconditions(action_str):
    try:
        # Extract the preconditions code block
        preconditions_block = extract_code_block('Precondition', action_str)
        # add indent
        lines = preconditions_block.splitlines()
        indented_lines = [lines[0]] + ['        ' + line for line in lines[1:]]
        preconditions_block = '\n'.join(indented_lines)
        return preconditions_block
    except Exception as e:
        print(f"Error parsing preconditions: {e}")
        showing_action_str = re.search(r'Response:\s*(.+)', action_str, re.IGNORECASE | re.DOTALL).group(1)
        print(f"Content:\n {showing_action_str}")
        print("Please input the correct preconditions string: ")
        return user_input_func()

def helper_parse_action_effects(action_str):
    try:
        # Extract the effects code block
        effects_block = extract_code_block('Effect', action_str)
        # add indent but not the first line
        lines = effects_block.splitlines()
        indented_lines = [lines[0]] + ['        ' + line for line in lines[1:]]
        effects_block = '\n'.join(indented_lines)
        return effects_block
    except Exception as e:
        print(f"Error parsing effects: {e}")
        showing_action_str = re.search(r'Response:\s*(.+)', action_str, re.IGNORECASE | re.DOTALL).group(1)
        print(f"Content:\n {showing_action_str}")
        print("Please input the correct effects string: ")
        return user_input_func()
        

def extract_code_block(section_title, action_str):
    pattern = rf'\*?\*?{section_title}s?:?\*?\*?:?\s*```(.*?)```'
    match = re.search(pattern, action_str, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError(f"Unable to find the section: {section_title}")
    
    
def helper_parse_action_parameters(action_str):
    try:
        # Match the Parameters section
        parameters_match = re.search(r'\*?\*?Parameters:?\*?\*?:?\s*(.+)(?=\s*Preconditions:)', action_str, re.IGNORECASE | re.DOTALL)
        if parameters_match:
            parameters_block = parameters_match.group(1).strip()
            # Use regex to find all parameter definitions
            parameters = re.findall(r'''(?:\d+\.\s*|-\s*)(\?[^;:\s"'\(\)]+)\s*\-\s*([^;:\s"\(\)"']+)''',
                                    parameters_block, re.IGNORECASE | re.DOTALL)
            parameters = [match for match in parameters if not match[1].lower().startswith(("this", "the"))]
            # Convert to the desired format
            parameters_str = ' '.join([f'{param[0]} - {param[1]}' for param in parameters])
            return f'({parameters_str})'
            
        else:
            raise ValueError("Unable to parse parameters.")
    except Exception as e:
        print(f"Error parsing parameters: {e}")
        # show after Response
        showing_action_str = re.search(r'Response:\s*(.+)', action_str, re.IGNORECASE | re.DOTALL).group(1)
        print(f"Content:\n {showing_action_str}")
        print("Please input the correct parameters string: ")
        return user_input_func()
    
if __name__ == "__main__":
    sample_str = """**Explanation:**

The "take-from-table" action is a fundamental part of managing books within a library. It represents the physical act of a librarian picking up a book from a table. For this action to be executed, certain conditions must be met to ensure the librarian can successfully pick up the book.

Firstly, the book must be on the table (`on-table ?x`). Secondly, the book needs to be accessible, meaning it's not obscured or covered by another book (`accessible ?x`). Lastly, the librarian's hands must be free to pick up the book (`hands-free`).

Once these preconditions are satisfied, the librarian can perform the action, which results in the book being held by the librarian (`holding ?x`). This action also implicitly assumes that once a book is held, it is no longer on the table, so the `on-table ?x` predicate becomes false.

**Response:**
Parameters:
1. ?x - book: [short description of the parameter representing the book to be taken from the table]

2. ?y - book: asdfs
- ?z - type ;;; asfsadf
- ?d - type;;; asdfasd 
- ?pp - This is a parameter


Preconditions:
```
(and
    (on-table ?x)
    (accessible ?x)
    (hands-free)
)
```

Effects:
```
(and
    (not (on-table ?x))
    (holding ?x)
)
```
"""
    print("Parameters:")
    print(helper_parse_action_parameters(sample_str))
    print("Preconditions:")
    print(helper_parse_action_preconditions(sample_str))
    print("Effects:")
    print(helper_parse_action_effects(sample_str))
    print("If the parsing is correct, show the action string:")
    showing_action_str = re.search(r'Response:\s*(.+)', sample_str, re.IGNORECASE | re.DOTALL).group(1)
    print(f"Content: {showing_action_str}")
    
    
# TODO the snippet output layout is not correct 