"""
This is a boilerplate pipeline 'compare_cos_sim_between_act_and_nl_desc'
generated using Kedro 0.19.6
"""
from copy import deepcopy
import json
import random
from typing import Sequence
import openai
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

from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.llm_utils import get_api_key
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str


def local_cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# come up with the box plot and dataframe csv 
class PAIR_TYPE(Enum):
    POSITIVE = "Positive (Correct Match)"
    EASY_NEGATIVE = "Easy Negative (Inter-Domain Mismatch)"
    SEMI_HARD_NEGATIVE = "Semi-Hard Negative (Intra-Domain Mismatch)"
    HARD_NEGATIVE = "Hard Negative (Manipulated Action)"

class COMPARING_SETTING(Enum):
    NL_DESC_VS_ACTION_SCHEMA = "NL Desc vs. Action Schema"
    EXPLANATION_VS_ACTION_SCHEMA = "Explanation vs. Action Schema" # the Explanation here is the query explanation, which means if the action is negative, the explanation will not fit the action schema
    NL_DESC_VS_EXPLANATION_ACTION_SCHEMA = "NL Desc vs. Explanation + Action Schema"
    # the explanation here is the answer explanation, which means if the action is negative, the explanation will also be negative that fits the action schema

# ! NODE
def analyzing_cos_sim_between_action_and_nl_desc(cross_encoder_model, setup_sentence_encoder_cfg):
    
    def local_comparing_setting_helper(
        answer_action_lst: Sequence[Action],
        query_content_dict: dict,
        comparing_setting: COMPARING_SETTING,
        pair_type_str: str,
        query_action_schema_str: str,
        query_explanation: str,
        answer_explanation_lst: Sequence[str],
        query_domain_name,
        query_action_name,
        df: pd.DataFrame,
        if_complex_context: bool = False, 
        **kwargs,
    ):
        nonlocal cross_encoder_model
        nonlocal setup_sentence_encoder_cfg

        alternative_embedding_model = None 
        if "activate_alternative_embedding" in setup_sentence_encoder_cfg:
            if setup_sentence_encoder_cfg["activate_alternative_embedding"]:
                alternative_embedding_model = setup_sentence_encoder_cfg['alternative_embedding_model']
        


        if "manipulation_details_lst" in kwargs:
            manipulation_details_lst = kwargs["manipulation_details_lst"]
        else:
            manipulation_details_lst = None
        # we will update the dataframe and return the updated dataframe
        if comparing_setting == COMPARING_SETTING.NL_DESC_VS_ACTION_SCHEMA:
            query_content = query_content_dict['context'] if if_complex_context else SIMPLER_PROMPT_CONTEXT + query_content_dict['query']
        elif comparing_setting == COMPARING_SETTING.EXPLANATION_VS_ACTION_SCHEMA:
            query_content =  query_content_dict['context'] if if_complex_context else SIMPLER_PROMPT_CONTEXT + query_content_dict['query'] + "\n" + query_explanation
        elif comparing_setting == COMPARING_SETTING.NL_DESC_VS_EXPLANATION_ACTION_SCHEMA:
            query_content = query_content_dict['context'] if if_complex_context else SIMPLER_PROMPT_CONTEXT + query_content_dict['query']
        
        answer_content_lst = [] 
        for answer_action, answer_explanation in zip(answer_action_lst, answer_explanation_lst):
            if comparing_setting == COMPARING_SETTING.NL_DESC_VS_ACTION_SCHEMA:
                answer_content = get_action_schema_answer_str(answer_action)
            elif comparing_setting == COMPARING_SETTING.EXPLANATION_VS_ACTION_SCHEMA:
                answer_content = get_action_schema_answer_str(answer_action)
            elif comparing_setting == COMPARING_SETTING.NL_DESC_VS_EXPLANATION_ACTION_SCHEMA:
                answer_content = answer_explanation + "\n" + get_action_schema_answer_str(answer_action)
            answer_content_lst.append(answer_content)
            
        # we run the model
        if alternative_embedding_model is None:
            query_embedding = cross_encoder_model.encode(query_content, convert_to_tensor=True)
            corpus_embeddings = cross_encoder_model.encode(answer_content_lst, convert_to_tensor=True)
            similarity_scores = cross_encoder_model.similarity(query_embedding, corpus_embeddings).detach().cpu().numpy().tolist()[0]
        else:
            api_key = get_api_key('openai')
            client = openai.OpenAI(
                api_key=api_key
            )
            all_content = [query_content] + answer_content_lst
            embeddings = client.embeddings.create(input=all_content, model=alternative_embedding_model).data

            query_embedding = embeddings[0]
            corpus_embeddings = embeddings[1:]
            query_embedding = query_embedding.embedding
            corpus_embeddings = [embedding.embedding for embedding in corpus_embeddings]
            similarity_scores = [local_cosine_similarity(query_embedding, corpus_embedding) for corpus_embedding in corpus_embeddings]
            


        
        # add to df
        new_row_dict = {
            'Domain': [query_domain_name] * len(answer_action_lst),
            "Action Name": [query_action_name] * len(answer_action_lst),
            "Cosine Sim Score": similarity_scores,
            "Pair Type": [pair_type_str] * len(answer_action_lst),
            "Comparison Mode": [comparing_setting.value] * len(answer_action_lst),
            "Query Content": [query_content] * len(answer_action_lst),
            "Answer Content": answer_content_lst,
            "Query Action Schema": [query_action_schema_str] * len(answer_action_lst),
            "Manipulation Details": manipulation_details_lst,
        } 
        df = pd.concat([df, pd.DataFrame(new_row_dict)], ignore_index=True)
        
        return df
        
            
    
    validation_domain_dirs = os.path.join(os.environ['WORKING_DIR'], "data/01_raw/pddl_domain/validation_set")
    
    # init dataframe 
    df = pd.DataFrame(columns=['Domain', "Action Name", "Cosine Sim Score", "Pair Type", "Comparison Mode", "Query Content", "Answer Content", "Query Action Schema", "Manipulation Details"])
    # * Setting: indicate the experimental setting, such as "Natural Language vs. Action Schema," "Explanation vs. Action Schema," or "Natural Language vs. Explanation + Action Schema."
    # * Pair Type: This column will categorize the type of comparison as "Positive (Correct Match)," "Easy Negative (Inter-Domain Mismatch)," "Semi-Hard Negative (Intra-Domain Mismatch)," or "Hard Negative (Match with Manipulated Action)."
    
    domain_filepaths = glob(os.path.join(validation_domain_dirs, f"**/domain_groundtruth.pddl"), recursive=True)
    for domain_filepath in tqdm(domain_filepaths, desc="Processing Domain"):
        domain_name = os.path.basename(os.path.dirname(domain_filepath))
        with open(domain_filepath, 'r') as f:
            domain_str = f.read()
        domain_model = DomainParser()(domain_str)
        action_model_list = list(domain_model.actions)
        action_to_query_dict = get_llm_input_dict(
            query_domain_name = domain_name,
            desc_granularity = "detailed",
            if_cot_in_fewshot = False,
        )
        explanation_fp = os.path.join(os.path.dirname(domain_filepath), "cot.json")
        with open(explanation_fp, 'r') as f:
            explanation_data = json.load(f)
        for query_action_model in tqdm(action_model_list, desc=f"Processing {domain_name} Actions", leave=False):
            query_action_name = query_action_model.name
            query_action_schema_str = str(query_action_model)
            query_content_temp_dict = action_to_query_dict[query_action_name]
            query_explanation = explanation_data[query_action_name]
            
            for pair_type in list(PAIR_TYPE):
                for comparing_setting in list(COMPARING_SETTING):
                    pair_type_str = pair_type.value
                    if pair_type == PAIR_TYPE.POSITIVE:
                        answer_action_lst = [query_action_model]
                        answer_explanation_lst = [query_explanation]
                    elif pair_type == PAIR_TYPE.EASY_NEGATIVE:
                        # get other domain's 
                        other_domain_filepaths = deepcopy(domain_filepaths)
                        other_domain_filepaths.remove(domain_filepath)
                        # randomly select one domain
                        other_domain_fp = random.choice(other_domain_filepaths)
                        answer_action_lst = []
                        answer_explanation_lst = [] 
                        with open(other_domain_fp, 'r') as f:
                            other_domain_str = f.read()
                        other_domain_model = DomainParser()(other_domain_str)
                        other_action_model_list = list(other_domain_model.actions)
                        other_domain_explanation_fp = os.path.join(os.path.dirname(other_domain_fp), "cot.json")
                        with open(other_domain_explanation_fp, 'r') as f:
                            other_explanation_data = json.load(f)
                        for other_action_model in other_action_model_list:
                            answer_explanation_lst.append(other_explanation_data[other_action_model.name])
                            answer_action_lst.append(other_action_model)
                                
                    elif pair_type == PAIR_TYPE.SEMI_HARD_NEGATIVE:
                        # get other actions in the same domain
                        answer_action_lst = deepcopy(action_model_list)
                        answer_action_lst.remove(query_action_model)
                        answer_explanation_lst = [] 
                        for other_action_model in answer_action_lst:
                            answer_explanation_lst.append(explanation_data[other_action_model.name])
                    elif pair_type == PAIR_TYPE.HARD_NEGATIVE:
                        # manipulate the action size 10 
                        answer_action_lst, manipulation_details_lst = get_manipulated_action_lst(
                            action_model = query_action_model, 
                            manipulated_action_num = 10, 
                            pollution_cap = 2, 
                        )
                        answer_explanation_lst = [query_explanation] * len(answer_action_lst)
                        
                        
                    comparing_helper_input_dict = dict(
                        answer_action_lst=answer_action_lst,
                        query_content_dict=query_content_temp_dict,
                        comparing_setting=comparing_setting,
                        pair_type_str=pair_type_str,
                        query_action_schema_str=query_action_schema_str,
                        query_explanation = query_explanation,
                        answer_explanation_lst = answer_explanation_lst,
                        query_domain_name = domain_name,
                        query_action_name=query_action_name,
                        df=df,
                    )
                    if pair_type == PAIR_TYPE.HARD_NEGATIVE:
                        comparing_helper_input_dict["manipulation_details_lst"] = manipulation_details_lst
                    
                    df = local_comparing_setting_helper(**comparing_helper_input_dict)
                    
    print("Length of the dataframe:", len(df))
    return df

# ! NODE 
def generate_boxplot_from_cos_sim_data(cosine_sim_comparison_data):
    change_dict = {
        "Explanation vs. Action Schema" : "Desc + Explanation vs. Action Schema",
    }
    cosine_sim_comparison_data['Comparison Mode'] = cosine_sim_comparison_data['Comparison Mode'].apply(lambda x: change_dict.get(x, x))
    
    # drop rows where Comparison Mode is "NL Desc vs. Explanation + Action Schema"
    cosine_sim_comparison_data_w_wo_exp = cosine_sim_comparison_data[cosine_sim_comparison_data['Comparison Mode'] != "NL Desc vs. Explanation + Action Schema"]
    
    cosine_sim_comparison_data_vs_exp_n_action = cosine_sim_comparison_data[cosine_sim_comparison_data['Comparison Mode'] == "NL Desc vs. Explanation + Action Schema"]
    
    # ! seaborn box plot
    fig1, ax = plt.subplots(figsize=(10, 5))
    sns.violinplot(data=cosine_sim_comparison_data_w_wo_exp, ax=ax, hue='Pair Type', x='Comparison Mode', y='Cosine Sim Score')
    # set y axis limit 
    # ax.set_ylim(0.4, 1.0)
    # force put hue legend at right bottom 
    ax.legend(loc='lower right')
    plt.title(f"Distribution of Cos-Sim Scores between `Natural Language Description` and `Action Schema`")
    
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    
    sns.violinplot(data=cosine_sim_comparison_data_vs_exp_n_action, ax=ax2, hue='Pair Type', x='Comparison Mode', y='Cosine Sim Score')
    plt.title(f"Distribution of Cos-Sim Scores between\n`NL Description` and `Explanation + Action Schema`")
    
    return fig1, fig2
    
    