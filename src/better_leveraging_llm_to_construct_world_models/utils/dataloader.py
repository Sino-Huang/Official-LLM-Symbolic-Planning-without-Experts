import importlib.util
import sys
import os 
from glob import glob
from better_leveraging_llm_to_construct_world_models.prompt_template.explain_template import *
from pddl.parser.domain import DomainParser
import json 

from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_domain_action_schema




def obtain_cot_few_shot_examples_from_llm():
    data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain')
    domain_file_pattern = os.path.join(data_dir, "**/domain_groundtruth.pddl")
    domain_filepaths = glob(domain_file_pattern, recursive=True)
    for domain_filepath in domain_filepaths:
        parent_dir = os.path.dirname(domain_filepath)
        data_py_fp = os.path.join(parent_dir, "data.py")
        # save the response to a file
        save_cot_response_path = os.path.join(parent_dir, "cot.json")
        # check if save_cot_response_path exists, we continue 
        if os.path.exists(save_cot_response_path):
            print(f"Skip {os.path.basename(parent_dir)}")
            continue
        print(domain_filepath)
        data_info_module = import_from_filepath(data_py_fp)
        
        
        
        # now we form context and query to get CoT few shot examples 
        context = COT_CONTEXT_FOR_EXPLANATION + COT_OBJECTIVE_FOR_EXPLANATION + COT_STYLE_FOR_EXPLANATION + COT_TONE_FOR_EXPLANATION + COT_AUDIENCE_FOR_EXPLANATION + COT_RESPONSE_FOR_EXPLANATION
        with open(domain_filepath, 'r') as f:
            domain_str = f.read()
        domain_model = DomainParser()(domain_str)
        action_schema = get_domain_action_schema(domain_model)
        
        cot_response_dict = dict()
        
        for action in action_schema:
            query = construct_query_for_explanation(
                domain_nl_desc = data_info_module.DOMAIN_DESC,
                action_nl_desc = data_info_module.ACTION_DESC_DICT[action.name]['detailed'],
                action_name = action.name,
                predicate_desc_lst = data_info_module.PREDICATE_DESC_LST,
                pddl_action_schema = str(action),
            )
            
            input_to_llm = context + "\n" + query
            print("Input to LLM:")
            print(input_to_llm)
            
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError: # press ctrl+d
                    break
            response = '\n'.join(lines)
            
            print("\n\n\n")
            print(response)
            input("Press Enter to continue...")
            print("\n\n\n\n\n")

            
            cot_response_dict[action.name] = response
            
        
        
        with open(save_cot_response_path, 'w') as f:
            json.dump(cot_response_dict, f, indent=4)

if __name__ == "__main__":
    obtain_cot_few_shot_examples_from_llm()