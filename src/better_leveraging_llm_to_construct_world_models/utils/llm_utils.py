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
import openai 

def get_api_key(model_type):
    conf_path = str(Path(os.environ['WORKING_DIR']) / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path)
    credentials = conf_loader["credentials"]
    return credentials['api_key'][model_type]


def llm_chat_completion_query(model_name, api_key, messages, top_p, temperature, max_tokens, web_search=True):
    if "glm" in model_name:
        client = ZhipuAI(api_key=api_key)
        
        input_dict = dict(
            model=model_name,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        if not web_search:
            input_dict['tools'] = [
                {
                    "type": "web_search",
                    "web_search":{
                        "enable": False,
                    },
                }
            ]

        response = client.chat.completions.create(
            **input_dict
        )
        return response
    elif "gpt" in model_name:
        client = openai.OpenAI(
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        
        return response