"""
This is a boilerplate pipeline 'finetuning_sentence_encoder'
generated using Kedro 0.19.6
"""

import logging
import sys
import traceback
from datetime import datetime
import os
import torch.nn.functional as F
from datasets import load_dataset
from datasets import Dataset
from sentence_transformers import SentenceTransformer, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.similarity_functions import SimilarityFunction
from sentence_transformers.trainer import SentenceTransformerTrainer
from sentence_transformers.training_args import BatchSamplers, SentenceTransformerTrainingArguments
from pathlib import Path
from tqdm.auto import tqdm 
from icecream import ic

from better_leveraging_llm_to_construct_world_models.pipelines.compare_cos_sim_between_act_and_nl_desc.nodes import COMPARING_SETTING, PAIR_TYPE
from .finetune_dataset import create_eval_dataset, create_test_dataset, create_train_dataset
import torch as th
import seaborn as sns 
from copy import deepcopy
import json
import random
from typing import Sequence
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 
from glob import glob 
from pddl.parser.domain import DomainParser
from enum import Enum
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect

from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import SIMPLER_PROMPT_CONTEXT, get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath
from better_leveraging_llm_to_construct_world_models.utils.pddl_manipulation import get_manipulated_action_lst
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str

from better_leveraging_llm_to_construct_world_models.pipelines.setup_sentence_encoder.nodes import create_sentence_encoder_helper
from transformers import TrainerCallback

class EarlyStoppingCallback(TrainerCallback):
    def __init__(self, early_stopping_patience: int, early_stopping_threshold: float):
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_threshold = early_stopping_threshold
        self.best_score = None
        self.patience_counter = 0

    def on_evaluate(self, args, state, control, **kwargs):
        eval_metric = kwargs.get("metrics", {}).get("eval_loss", None)  # Replace eval_loss with your evaluation metric
        if eval_metric is not None:
            if self.best_score is None or eval_metric < self.best_score + self.early_stopping_threshold:
                self.best_score = eval_metric
                self.patience_counter = 0
                print(f"Best score: {self.best_score}")
            else:
                self.patience_counter += 1
                print(f"Patience counter: {self.patience_counter}")
                if self.patience_counter >= self.early_stopping_patience:
                    print("Early stopping triggered")
                    control.should_training_stop = True

# ! NODE
def train_sentence_encoder(setup_sentence_encoder_cfg, finetuning_encoder_cfg, cosine_sim_comparison_data):
    # Set the log level to INFO to get more information
    train_batch_size = finetuning_encoder_cfg['train_batch_size']
    eval_negative_weights = finetuning_encoder_cfg['eval_negative_weights']
    train_negative_weights = finetuning_encoder_cfg['train_negative_weights']
    training_epoch = finetuning_encoder_cfg['training_epoch']
    is_finetune_complete = finetuning_encoder_cfg['is_finetune_complete']
    
    


    # 1. Here we define our SentenceTransformer model. If not already a Sentence Transformer model, it will automatically
    # create one with "mean" pooling.
    if not is_finetune_complete:
        model_name = setup_sentence_encoder_cfg['model_name']
        sentence_model = SentenceTransformer(model_name)
        # Save path of the model
        output_dir = os.path.join(os.environ['WORKING_DIR'], "data/06_models", f"finetuned_sentence_encoder_batch_{train_batch_size}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        print(f"Model will be saved at: {output_dir}")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # 2. Load the dataset:
        train_dataset = create_train_dataset()
        # output of train_dataset is a dictionary with keys: ['anchor', 'positive', 'negative']
        eval_dataset = create_eval_dataset()

        # 3. Define our training loss: https://sbert.net/docs/package_reference/sentence_transformer/losses.html#gistembedloss
        # The guiding model
        if False and setup_sentence_encoder_cfg['model_name'].split('/')[-1] in ["sentence-t5-xl", 'gtr-t5-xl', 'all-roberta-large-v1']:
            print("Using MultipleNegativesRankingLoss")
            train_loss = losses.MultipleNegativesRankingLoss(sentence_model)
        else:
            print("Using GISTEmbedLoss")
            guide_model = SentenceTransformer("sentence-transformers/sentence-t5-xl")
            if model_name == "google/flan-t5-xl":
                sentence_model.max_seq_length = guide_model.max_seq_length
                print("Setting max_seq_length to", sentence_model.max_seq_length)
            train_loss = losses.GISTEmbedLoss(sentence_model, guide_model)


        num_examples = train_dataset.info.splits["train"].num_examples
        # 5. Define the training arguments
        # ref: https://github.com/UKPLab/sentence-transformers/pull/2792
        args = SentenceTransformerTrainingArguments(
            # Required parameter:
            output_dir=output_dir,
            # Optional training parameters:
            per_device_train_batch_size=train_batch_size,
            # learning_rate=2e-5,
            warmup_ratio=0.1,
            fp16=True,  # Set to False if you get an error that your GPU can't run on FP16
            bf16=False,  # Set to True if you have a GPU that supports BF16
            batch_sampler=BatchSamplers.NO_DUPLICATES,
            # Optional tracking/debugging parameters:
            eval_strategy="steps",
            save_strategy="steps",
            save_steps=50,
            eval_steps=50,
            num_train_epochs=training_epoch,
            max_steps = num_examples * training_epoch // train_batch_size,
            save_total_limit=10,
            logging_steps=10,
            logging_first_step=True,
            run_name=f"batch_{train_batch_size}_finetune_sentence_encoder_on_{setup_sentence_encoder_cfg['model_name'].split('/')[-1]}",  
            # Will be used in W&B if `wandb` is installed
        )


        # 6. Create the trainer & start training
        trainer = SentenceTransformerTrainer(
            model=sentence_model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            loss=train_loss,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=8, early_stopping_threshold=0.05)]
        )
        trainer.train()
        
        # 8. Save the trained & evaluated model locally
        final_output_dir = f"{output_dir}/final"
        Path(final_output_dir).mkdir(parents=True, exist_ok=True)
        sentence_model.save(final_output_dir)
        
    if finetuning_encoder_cfg['best_model_path'] is not None:
        best_model_path = os.path.join(os.environ['WORKING_DIR'], finetuning_encoder_cfg['best_model_path'])
        sentence_model = SentenceTransformer(best_model_path)
        

    # 7. Evaluate the model performance on the STS Benchmark test dataset
    test_dataset = create_test_dataset(cosine_sim_comparison_data)
    test_output_dict= {
        'Domain' : [],
        'Action Name' : [],
        'Pair Type' : [],
        'Comparison Mode' : [],
        'Query Content' : [],
        'Answer Content' : [],
        'Cosine Sim Score' : []
    }
    query_text = []
    answer_text = []
    for test_data in tqdm(test_dataset, desc="Evaluating on test dataset"):
        domain = test_data['Domain']
        action_name = test_data['Action Name']
        pair_type = test_data['Pair Type']
        comparison_mode = test_data['Comparison Mode']
        query_content = test_data['Query Content']
        answer_content = test_data['Answer Content']
        test_output_dict['Domain'].append(domain)
        test_output_dict['Action Name'].append(action_name)
        test_output_dict['Pair Type'].append(pair_type)
        test_output_dict['Comparison Mode'].append(comparison_mode)
        test_output_dict['Query Content'].append(query_content)
        test_output_dict['Answer Content'].append(answer_content)
        query_text.append(query_content)
        answer_text.append(answer_content)
        
    chunksize = 32
    for i in range(0, len(query_text), chunksize):
        query_chunk = query_text[i:i+chunksize]
        answer_chunk = answer_text[i:i+chunksize]
        query_embedding = sentence_model.encode(query_chunk, convert_to_tensor=True)
        answer_embedding = sentence_model.encode(answer_chunk, convert_to_tensor=True)
        with th.no_grad():
            similarity_scores = F.cosine_similarity(query_embedding, answer_embedding)
        for j, score in enumerate(similarity_scores):
            test_output_dict['Cosine Sim Score'].append(score.item())
            
    # form the dataframe
    validation_set_testing_output_df = pd.DataFrame(test_output_dict)
    
    
    testing_set_testing_output_df = generate_testing_domains_eval_df(sentence_model)
    
    return validation_set_testing_output_df, testing_set_testing_output_df


# ! NODE 
# TODO 
def generate_plot_from_finetuned_model(validation_set_cosine_sim_comparison_data_after_finetune, testing_set_cosine_sim_comparison_data_after_finetune):
    change_dict = {
        "Explanation vs. Action Schema" : "Desc + Explanation vs. Action Schema",
    }
    validation_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'] = validation_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'].apply(lambda x: change_dict.get(x, x))
    
    # ! seaborn box plot
    fig1, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=validation_set_cosine_sim_comparison_data_after_finetune, ax=ax, hue='Pair Type', x='Comparison Mode', y='Cosine Sim Score')
    # set y axis limit 
    # ax.set_ylim(0.4, 1.0)
    # force put hue legend at right bottom 
    ax.legend(loc='lower right')
    plt.title(f"Distribution of Cos-Sim Scores between\n`NL Desc.` and `Action Schema`\nUsing Finetuned Sentence Encoder")
    
    
    # same for testing_set_cosine_sim_comparison_data_after_finetune
    
    fig2, ax = plt.subplots(figsize=(7, 5))
    change_dict = {
        "Explanation vs. Action Schema" : "Desc + Explanation vs. Action Schema",
    }
    testing_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'] = testing_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'].apply(lambda x: change_dict.get(x, x))
    
    # drop 
    testing_set_cosine_sim_comparison_data_after_finetune = testing_set_cosine_sim_comparison_data_after_finetune[testing_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'] == "NL Desc vs. Action Schema"]
    # drop rows where Comparison Mode is "NL Desc vs. Explanation + Action Schema"
    testing_set_cosine_sim_comparison_data_after_finetune = testing_set_cosine_sim_comparison_data_after_finetune[testing_set_cosine_sim_comparison_data_after_finetune['Comparison Mode'] != "NL Desc vs. Explanation + Action Schema"]
    
    sns.boxplot(data=testing_set_cosine_sim_comparison_data_after_finetune, ax=ax, hue='Pair Type', x='Comparison Mode', y='Cosine Sim Score')
    # set y axis limit 
    # ax.set_ylim(0.4, 1.0)
    # force put hue legend at right bottom 
    ax.legend(loc='lower right')
    plt.title(f"Distribution of Cos-Sim Scores between\n`NL Desc.` and `Action Schema`\nUsing Finetuned Sentence Encoder")
   
    return fig1, fig2



def generate_testing_domains_eval_df(finetuned_model):
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
        query_embedding = finetuned_model.encode(query_content, convert_to_tensor=True)
        corpus_embeddings = finetuned_model.encode(answer_content_lst, convert_to_tensor=True)
        similarity_scores = finetuned_model.similarity(query_embedding, corpus_embeddings).detach().cpu().numpy().tolist()[0]
        
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
        
            
    
    testing_domain_dirs = os.path.join(os.environ['WORKING_DIR'], "data/01_raw/pddl_domain/testing_set")
    
    # init dataframe 
    df = pd.DataFrame(columns=['Domain', "Action Name", "Cosine Sim Score", "Pair Type", "Comparison Mode", "Query Content", "Answer Content", "Query Action Schema", "Manipulation Details"])
    # * Setting: indicate the experimental setting, such as "Natural Language vs. Action Schema," "Explanation vs. Action Schema," or "Natural Language vs. Explanation + Action Schema."
    # * Pair Type: This column will categorize the type of comparison as "Positive (Correct Match)," "Easy Negative (Inter-Domain Mismatch)," "Semi-Hard Negative (Intra-Domain Mismatch)," or "Hard Negative (Match with Manipulated Action)."
    
    domain_filepaths = glob(os.path.join(testing_domain_dirs, f"**/domain_groundtruth.pddl"), recursive=True)
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