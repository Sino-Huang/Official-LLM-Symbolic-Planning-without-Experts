import os
import random
from pddl.parser.domain import DomainParser
from pddl.core import Domain
import json
from glob import glob


from better_leveraging_llm_to_construct_world_models.utils.import_py import import_from_filepath


PLAN_PROMPT_CONTEXT = """# CONTEXT #
You are a tool called Automated Planning Action Planner. 
You are a technical expert in constructing and evaluating the quality of action plans via the natural language context.
"""

PLAN_PROMPT_OBJECTIVE = """# OBJECTIVE #
* Add only one more action to the given action plan sequence towards achieving the goal state.
* Provide the action name and the objects that this action will interact with.
* Evaluate the confidence score that continuing with the suggested action plan will eventually lead to the goal state.
* Determine if the action plan has already reached the goal state.
* Output only one action at each step and stop.
* You should think step by step, you think think more steps. 
"""

PLAN_PROMPT_STYLE = """# STYLE #
Follow the writing style of technical experts. The output can be parsed by a machine, so it is important to follow the structured format.
"""

PLAN_PROMPT_TONE = """# TONE #
Be precise and concise in constructing the action plan sequence. Provide clear information about the objects involved, the numerical confidence score, and the boolean value for the goal state check.
"""

PLAN_PROMPT_AUDIENCE = """# AUDIENCE #
Your audience is someone who is asking for a detailed action plan to solve sequential decision making problems. 
"""

PLAN_PROMPT_RESPONSE = """# RESPONSE #
The response should be in the following format:
---
**Response:**
1. Action {n}: [Action Name]
2. Objects: 
   - ?x - [type]: [object description]
   - ...
   
3. Updated Action Plan: 
   - [Action 1 and the objects involved] 
   - [Action 2 and the objects involved]
   - ...
   - [Action {n} and the objects involved]

**Confidence Evaluation:**
[Analyze the updated action plan, then at the last line conclude "The confidence score is {s}", where s is an integer from 1 to 10]

**Goal State Check:**
[Briefly analyze the current state, then at the last line conclude "The planning is continuing" or "The planning is completed"]
---
"""


def construct_query_for_planning(
    domain_nl_desc, action_nl_desc, predicate_desc_lst, init_state_desc, goal_desc, object_snippet_str, current_action_plan_str,
):

    # add line number to each predicate description and join them using \n
    predicate_desc_str = "\n".join(
        [f"{i+1}. {predicate}" for i, predicate in enumerate(predicate_desc_lst)]
    )

    output = f"""Question: Here is the task.
A natural language description of the domain
Domain information: {domain_nl_desc}

A list of available predicates
{predicate_desc_str}

Action Description: 
{action_nl_desc}

Problem Information: 

Object Snippet: {object_snippet_str}

Initial State: {init_state_desc}

Goal State: {goal_desc}

Current Action Plan:
{current_action_plan_str}

Your answer:
"""
    return output


def get_llm_input_for_planning(query_domain_name,
                               desc_granularity,
                               current_action_plan_str = "Empty",
                               verbose=False, 
                               ):
    """
    Get the input dictionary for the LLM model for the planning task.
    """
    query_domain_dir_lst = glob(
        os.path.join(
            os.environ["WORKING_DIR"],
            "data/01_raw/pddl_domain",
            f"*/{query_domain_name}",
        )
    )
    query_domain_dir = query_domain_dir_lst[0]
    if not os.path.exists(query_domain_dir):
        raise FileNotFoundError(
            f"Domain {query_domain_name} does not exist in the testing set."
        )
        
    query_domain_info = import_from_filepath(os.path.join(query_domain_dir, "data.py"))
    
    query_problem_info = import_from_filepath(os.path.join(query_domain_dir, "problem_info.py"))
    
    domain_nl_desc=query_domain_info.DOMAIN_DESC
    action_name_lst_path = os.path.join(query_domain_dir, "action_name_lst.json")
    if not os.path.exists(action_name_lst_path):
        # we load it from domain_groundtruth.pddl
        with open(os.path.join(query_domain_dir, "domain_groundtruth.pddl"), "r") as f:
            domain_str = f.read()
        domain_model: Domain = DomainParser()(domain_str)
        action_name_lst = [action.name for action in domain_model.actions]
        # save to file using json
        with open(action_name_lst_path, "w") as f:
            json.dump(action_name_lst, f, indent=4)
    else:
        with open(action_name_lst_path, "r") as f:
            action_name_lst = json.load(f)
    action_nl_desc = ""
    
    for action_name in action_name_lst:
        action_nl_desc += f"""Action Name: {action_name}\nAction Description: {query_domain_info.ACTION_DESC_DICT[action_name][desc_granularity]}\n\n"""
        
    predicate_desc_lst = query_domain_info.PREDICATE_DESC_LST
    init_state_desc = query_problem_info.INIT_STATE_DESC
    goal_desc = query_problem_info.GOAL_STATE_DESC
    object_snippet_str = query_problem_info.OBJECT_SNIPPET_STR
    
    output = dict()
    output["context"] = PLAN_PROMPT_CONTEXT+PLAN_PROMPT_OBJECTIVE+PLAN_PROMPT_STYLE+PLAN_PROMPT_TONE+PLAN_PROMPT_AUDIENCE+PLAN_PROMPT_RESPONSE
    output["query"] = construct_query_for_planning(
        domain_nl_desc = domain_nl_desc,
        action_nl_desc = action_nl_desc,
        predicate_desc_lst = predicate_desc_lst,
        init_state_desc = init_state_desc,
        goal_desc = goal_desc,
        object_snippet_str = object_snippet_str,
        current_action_plan_str = current_action_plan_str,
    )
    if verbose:
        print("\n\n\n")
        print(output["context"])
        print(output["query"])
        print("\n\n\n")
        
    return output


if __name__ == "__main__":
    query_domain = "libraryworld"
    desc_granularity = "detailed"
    ask_for_plan_query_dict = get_llm_input_for_planning(
        query_domain, desc_granularity, verbose=True, current_action_plan_str="Empty",
    )
    