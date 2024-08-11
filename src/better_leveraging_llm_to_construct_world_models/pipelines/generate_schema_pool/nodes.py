"""
This is a boilerplate pipeline 'generate_schema_pool'
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

from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.llm_utils import get_api_key, llm_chat_completion_query



def setup_query_message_dict_lst(query_domain, desc_granularity, if_cot_in_fewshot):
    """
    Sets up a query message dictionary list based on the given parameters.

    Args:
        query_domain (str): The query domain.
        desc_granularity (str): The description granularity.
        if_cot_in_fewshot (bool): Indicates whether the context of thought (COT) is included in the few-shot examples.

    Returns:
        dict: The query message dictionary list.

    """
    action_to_query_dict = get_llm_input_dict(
        query_domain, desc_granularity, if_cot_in_fewshot, verbose=False
    )
    output = dict()
    for action_name, action_dict in action_to_query_dict.items():
        output[action_name] = [] 
        
        context = action_dict['context']
        output[action_name].append(
            {
                "role": "system",
                "content": context
            }
        )
        
        fewshot_lst = action_dict['fewshot']
        for q_i in range(0, len(fewshot_lst), 2):
            a_i = q_i + 1
            output[action_name].append(
                {
                    "role": "user",
                    "content": fewshot_lst[q_i]
                }
            )
            output[action_name].append(
                {
                    "role": "assistant",
                    "content": fewshot_lst[a_i]
                }
            )
        
        query = action_dict['query']
        output[action_name].append({
            "role": "user",
            "content": query
        })
        
    return output

# ! NODE
def query_llm(general_cfg, generate_schema_pool_cfg):
    root_seed = general_cfg['seed']
    
    # env related 
    query_domain = general_cfg['query_domain']
    desc_granularity = general_cfg['desc_granularity']
    if_cot_in_fewshot = general_cfg['if_cot_in_fewshot']
    env_tag_name = f"{query_domain}_{desc_granularity}_cot_{if_cot_in_fewshot}"
    # ----
    
    model_name = generate_schema_pool_cfg['model_name']
    model_type = generate_schema_pool_cfg['model_type']
    top_p = generate_schema_pool_cfg['top_p']
    temperature = generate_schema_pool_cfg['temperature']
    max_tokens = generate_schema_pool_cfg['max_tokens']
    model_tag_name = f"{model_name}_top_p_{top_p}_temp_{temperature}_seed_{root_seed}"
    ensemble_size = generate_schema_pool_cfg['ensemble_size']
    
    
    # set seed 
    random.seed(root_seed)
    np.random.seed(root_seed)
    
    # set seed_lst based on ensemble_size
    seed_lst = np.random.randint(0, 10000, ensemble_size)
    
    api_key = get_api_key(model_type)
    save_dir = os.path.join(os.environ['WORKING_DIR'], 'data/07_model_output', "pure_generate_schema_pool", env_tag_name, model_tag_name)
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    for id, seed in enumerate(tqdm(seed_lst, desc='Querying LLMs')):
        # set seed
        random.seed(seed)
        np.random.seed(seed)
        
        # setup messages 
        messages_per_action_dict = setup_query_message_dict_lst(
            query_domain = query_domain,
            desc_granularity = desc_granularity,
            if_cot_in_fewshot = if_cot_in_fewshot,
        )
        for action_name in tqdm(messages_per_action_dict, desc=f"Working on id: {id}"):
            messages = messages_per_action_dict[action_name]
            response = llm_chat_completion_query(
                model_name = model_name,
                api_key = api_key,
                messages = messages,
                top_p = top_p,
                temperature = temperature,
                max_tokens = max_tokens
            )
            
            record_data = deepcopy(messages)
            # edit the data to include wether they are prompt or response 
            # messages are all prompt as we are querying the model
            for record in record_data:
                record['type'] = 'prompt'
                
            # add the response to the record_data
            response_dict = {
                "role": response.choices[0].message.role,
                "content": response.choices[0].message.content,
                "type": "response",
                "action": action_name
            }
            record_data.append(response_dict)
            save_path = os.path.join(save_dir, f"conversation_id_{id}.jsonl")
            # check if exists
            if os.path.exists(save_path):
                mode = 'a'
            else:
                mode = 'w'
            with open(save_path, mode) as f:
                for record in record_data:
                    f.write(json.dumps(record) + '\n')