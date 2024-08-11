"""
This is a boilerplate pipeline 'tree_of_thought_direct_planning'
generated using Kedro 0.19.6
"""

# ref: https://github.com/princeton-nlp/tree-of-thought-llm/blob/master/src/tot/prompts/text.py

from copy import deepcopy
from pathlib import Path
from datetime import datetime
import re
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
import os
from zhipuai import ZhipuAI
import random
import numpy as np
from icecream import ic
from tqdm.auto import tqdm
import json
from glob import glob
from collections import deque

from better_leveraging_llm_to_construct_world_models.prompt_template.tot_plan_template import (
    get_llm_input_for_planning,
)
from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner
from better_leveraging_llm_to_construct_world_models.utils.llm_utils import get_api_key, llm_chat_completion_query


# ! NODE
def query_plans_llm(general_cfg, tot_direct_planning_cfg):
    # env related
    query_domain = general_cfg["query_domain"]
    desc_granularity = general_cfg["desc_granularity"]
    env_tag_name = f"{query_domain}_{desc_granularity}"
    # ----

    model_name = tot_direct_planning_cfg["model_name"]
    model_type = tot_direct_planning_cfg["model_type"]
    top_p = tot_direct_planning_cfg["top_p"]
    temperature = tot_direct_planning_cfg["temperature"]
    max_tokens = tot_direct_planning_cfg["max_tokens"]
    tree_breadth = tot_direct_planning_cfg["tree_breadth"]
    tree_depth_ratio = tot_direct_planning_cfg["tree_depth_ratio"]
    model_tag_name = f"{model_name}_top_p_{top_p}_temp_{temperature}_tree_breadth_{tree_breadth}_depth_ratio_{tree_depth_ratio}"

    save_dir = os.path.join(
        os.environ["WORKING_DIR"],
        "data/07_model_output",
        "tree_of_thought_plans",
        env_tag_name,
        model_tag_name,
        datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
    )
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    api_key = get_api_key(model_type)

    # get the domain file
    domain_file_pattern = os.path.join(
        os.environ["WORKING_DIR"],
        "data/01_raw/pddl_domain",
        "**/domain_groundtruth.pddl",
    )
    domain_file_lst = glob(domain_file_pattern, recursive=True)

    domain_filepath = [f for f in domain_file_lst if query_domain in f][0]
    dir_path = os.path.dirname(domain_filepath)
    problem_paths = glob(os.path.join(dir_path, "p*.pddl"))

    for p_id, problem_path in enumerate(problem_paths):
        # get the groundtruth plan 
        groundtruth_result = call_pddl_planner(domain_filepath ,problem_path)
        if not groundtruth_result['is_ok']:
            raise ValueError(f"Error in getting groundtruth plan for problem: {problem_path}")
        groundtruth_plan = groundtruth_result['plan_lst']
        depth_limit = int(len(groundtruth_plan) * tree_depth_ratio)
        
        # get query data
        ask_for_plan_query_dict = get_llm_input_for_planning(
            query_domain,
            desc_granularity,
            verbose=False,
            current_action_plan_str="Empty",
        )
        context = ask_for_plan_query_dict["context"]
        query = ask_for_plan_query_dict["query"]

        # setup message note that this message will be updated in the loop
        initial_messages = [
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": query,
            },
        ]
        
        # Initialize the queue with the initial messages and the current depth
        queue = deque([(initial_messages, 0, 0)]) # (messages, current depth, accumulated heuristic)
        total_heuristic_values = []  # List to store total heuristic values of all terminal nodes
        total_plans = []  # List to store all plans
        
        plan_path_idx = 0 # Index to keep track of terminated plans 
        pbar = tqdm(desc=f"Querying LLM for plans, count: ")
        while len(queue) > 0:
            # # display all the plan_str_lst in the queue
            # for idx, (messages, _, _) in enumerate(queue):
            #     if 'plan_str_lst' in messages[-1]:
            #         print("")
            #         print(f"Plan {idx}: {messages[-1]['plan_str_lst']}")
                    
            # Get the current set of messages, depth, and accumulated heuristic from the queue
            messages, cur_depth, accumulated_heuristic = queue.popleft()
            if cur_depth >= depth_limit:
                total_heuristic_values.append(accumulated_heuristic)
                total_plans.append(messages[-1]["plan_str_lst"])
                save_plan_message(
                    messages = messages,
                    save_dir = save_dir,
                    p_id = p_id,
                    plan_path_idx = plan_path_idx,
                    accu_heuristic_val = accumulated_heuristic,
                )
                plan_path_idx += 1
                continue
            
            for breadth in tqdm(range(tree_breadth), desc="Breadth", leave=False):
                local_message = deepcopy(messages)
                local_message_simplified = simplify_message(local_message)
                response = llm_chat_completion_query(
                    model_name=model_name,
                    api_key=api_key,
                    messages=local_message_simplified,
                    top_p=top_p,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    web_search = False, 
                )
                pbar.update(1)
                                
                heuristic_val = parse_heuristic(response.choices[0].message.content) 
                is_terminated = parse_terminated(response.choices[0].message.content) or cur_depth >= depth_limit
                updated_plan_str_lst = parse_plan_str_lst(response.choices[0].message.content)
                # ! in case the llm will change the history, we only take the last one and concat with the previous ones
                if "plan_str_lst" in local_message[-1]:
                    updated_plan_str_lst = local_message[-1]["plan_str_lst"] + [updated_plan_str_lst[-1]]
                
                updated_accumulated_heuristic = accumulated_heuristic + heuristic_val
                
                response_dict = {
                    "role": response.choices[0].message.role,
                    "content": response.choices[0].message.content,
                    "type": "response",
                    "heuristic": heuristic_val,
                    "accumulated_heuristic": updated_accumulated_heuristic,
                    "is_terminated": is_terminated,
                    "plan_str_lst": updated_plan_str_lst,
                    "depth": cur_depth,
                }
                
                local_message.append(response_dict)
                
                # save the current tree 
                
                if is_terminated:
                    total_heuristic_values.append(updated_accumulated_heuristic)
                    total_plans.append(updated_plan_str_lst)
                    save_plan_message(
                        messages = local_message,
                        save_dir = save_dir,
                        p_id = p_id,
                        plan_path_idx = plan_path_idx,
                        accu_heuristic_val = updated_accumulated_heuristic,
                    )
                    plan_path_idx += 1
                    continue
                
                # also check if any queque contains the same plan_str_lst, we also continue 
                if_duplicate = False
                for in_queue_message, _, _ in queue:
                    if in_queue_message[-1]["plan_str_lst"] == updated_plan_str_lst:
                        if_duplicate = True
                        break
                if if_duplicate:
                    continue
                
                # add the updated message to the queue
                # ! add the new user query to the message 
                updated_plan_str_lst_str = "\n".join([f"- {x}" for x in updated_plan_str_lst])
                updated_plan_str_lst_str+= "\n"
                
                new_query = {
                    "role": "user",
                    "plan_str_lst": updated_plan_str_lst,
                    "content": f"""Current Action Plan:
{updated_plan_str_lst_str}

Continue your planning.
Your answer:

"""
                }
                
                local_message.append(new_query)
                
                queue.append((local_message, cur_depth + 1, updated_accumulated_heuristic))
                
        pbar.close()
        # save the summarized info 
        with open(os.path.join(save_dir, f"summary_for_problem_{p_id}.jsonl"), "w") as f:
            output = []
            for plan, heuristic in zip(total_plans, total_heuristic_values):
                output.append({
                    "plan": plan,
                    "heuristic": heuristic
                })
            # for each data, we get heuristic val and divide by the length of plan
            for d in output:
                d["heuristic"] = round(d["heuristic"] / len(d["plan"]), 2)
            # sort descending 
            output = sorted(output, key=lambda x: x["heuristic"], reverse=True)
            for d in output:
                f.write(json.dumps(d) + "\n")
                
        return None 

def simplify_message(messages):
    output = [] 
    for message in messages:
        output.append({
            "role": message['role'],
            "content": message['content']
        })
    return output

def save_plan_message(messages, save_dir, p_id, plan_path_idx, accu_heuristic_val):
    save_path = os.path.join(save_dir, f"plan_{plan_path_idx}_for_problem_{p_id}_score_{accu_heuristic_val}.jsonl")
    with open(save_path, "w") as f:
        for message in messages:
            f.write(json.dumps(message) + "\n")
            
            
            
def parse_heuristic(content_str):
    try:
        heuristic_match = re.search(r'confidence score is (\d+)', content_str, re.IGNORECASE)
        if heuristic_match:
            return int(heuristic_match.group(1))
        else:
            raise ValueError("Unable to parse heuristic value.")
    except Exception as e:
        print(f"Error parsing heuristic value: {e}")
        print(f"Content: {content_str}")
        return int(input("Please input the correct heuristic value: "))

def parse_terminated(content_str):
    try:
        goal_state_match = re.search(r'goal state check:?\*?\*?:?\s*(.+)', content_str, re.IGNORECASE)
        if goal_state_match:
            goal_state = goal_state_match.group(1).strip()
            assert 'the planning is completed' in goal_state.lower() or 'the planning is continuing' in goal_state.lower()
            return 'the planning is completed' in goal_state.lower()
        else:
            raise ValueError("Unable to parse goal state.")
    except Exception as e:
        print(f"Error parsing goal state: {e}")
        print(f"Content: {content_str}")
        user_input = input("Is the planning completed? (y/n): ").strip().lower()
        return user_input == 'y'

def parse_plan_str_lst(content_str):
    try:
        # Updated regex pattern to match section titles with optional **
        plan_match = re.search(r'\*?\*?updated action plan:?\*?\*?:?\s*(.*?)(\*?\*?confidence evaluation:?\*?\*?:?|\*?\*?goal state check:?\*?\*?:?|$)', content_str, re.IGNORECASE | re.DOTALL)
        if plan_match:
            plan_raw =  plan_match.group(1).strip()
        else:
            raise ValueError("Unable to parse updated action plan.")
    except Exception as e:
        print(f"Error parsing updated action plan: {e}")
        print(f"Content: {content_str}")
        print("Wanted format: '- take-from-table Book2\\n   - place-on-shelf Book2 onto Book3\\n   - take-from-table Book1\\n   - place-on-shelf Book1 onto Book2\\n\\n'")
        plan_raw = input("Please input the correct updated action plan: ")
        if plan_raw == "":
            return ['completed']
        
    # further process the plan_raw
    # notes: ?: is used to make the group non-capturing
    # notes: ?= Positive Lookahead -- Assert that the regex can be matched
    plan_actions = re.findall(r'(?:-\s*|\d+\.\s*)(.*?)\s*(?=\n|$)', plan_raw)
    return plan_actions
            
if __name__ == "__main__":
    example_content_str = """---
**Response:**
1. Action 1: take-from-table
2. Objects: 
   - Book2 - book: Book2 is on the table and accessible

3. Updated Action Plan: 
   - take-from-table Book2
   - place-on-shelf Book2 onto Book3
   - take-from-table Book1
   - place-on-shelf Book1 onto Book2

**Confidence Evaluation:**
The action plan is currently straightforward and involves taking the first step to achieve the goal state by ensuring Book2 is in hand. The confidence score is 8.

**Goal State Check:**
The planning is continuing. Book2 needs to be placed on top of Book3, and Book1 needs to be placed on top of Book2. The current action does not complete the goal state.
"""
    heuristic = parse_heuristic(example_content_str)
    print(heuristic)
    terminated = parse_terminated(example_content_str)
    print(terminated)
    plan_lst_str = parse_plan_str_lst(example_content_str)
    print(plan_lst_str)