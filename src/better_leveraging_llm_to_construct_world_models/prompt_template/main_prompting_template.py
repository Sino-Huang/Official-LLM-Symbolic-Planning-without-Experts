import os
from glob import glob
import random
from pddl.parser.domain import DomainParser
from pddl.core import Domain
import json

from better_leveraging_llm_to_construct_world_models.utils.import_py import (
    import_from_filepath,
)
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import (
    get_action_schema_answer_str,
    get_beautiful_effect_str,
    get_beautiful_parameter_str,
    get_beautiful_precondition_str,
)


SIMPLER_PROMPT_CONTEXT = "Context: Translate the given natural language description into an action schema that includes the parameters, preconditions, and effects. Ensure that only the provided predicates are used to construct the preconditions and effects.\n"

PROMPT_CONTEXT = """# CONTEXT #
You are a tool called PDDL Modeling Assistant. \
You are a technical experts in constructing Planning Domain Definition Language (PDDL) models via the natural language context.
"""

PROMPT_OBJECTIVE = """# OBJECTIVE #
* Construct parameters, preconditions and effects based on the domain information, action description and the action name.
* All variables in the preconditions and effects must be listed in the action's parameters. This restriction helps maintain the action's scope and prevents ambiguity in the planning process.
* Do not use predicates that are not defined in the available predicates list to construct the preconditions and effects.
* When the natural language description is ambiguous or certain predicate changes are implied, make reasonable assumptions based on common sense to fill up the implicit predicate in the PDDL action.
"""

PROMPT_STYLE = """# STYLE #
Follow the writing style of technical experts. The output can be parsed by a machine, so it is important to follow the structured format.
"""

PROMPT_TONE = """# TONE #
Be precise and concise in constructing the PDDL action. The PDDL action should be clear and unambiguous.
"""

PROMPT_AUDIENCE = """# AUDIENCE #
Your audience is someone who is trying to learn how to construct PDDL actions from natural language descriptions.
"""

PROMPT_RESPONSE = """# RESPONSE #
The response should be in the following format:
---
**Explanation:** [Your explanation here]

**Response:**
Parameters:
1. ?x - [type]: [parameter description]
2. ...

Preconditions:
```
(and
    ([predicate_1] ?x)
)
```

Effects:
```
(and
    (not ([predicate_2] ?x))
    ([predicate_2] ?x)
    ...
)
```
---
"""


def construct_query_for_modeling(
    domain_nl_desc, action_nl_desc, action_name, predicate_desc_lst
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

Action Description: {action_nl_desc}

Action name: {action_name}


Your answer:
"""
    return output


def construct_llm_input_dict_for_action_modeling(
    domain_nl_desc,
    action_nl_desc,
    action_name,
    predicate_desc_lst,
    if_cot_in_fewshot,
    fewshot_example_domain_dir_lst,
):
    # we will select two actions from each domain for the few-shot example, if if_cot_in_fewshot is True, we will also add the COT content in the few-shot example

    # load two fewshot domains
    few_shot_domain_lst = []
    for domain_dir in fewshot_example_domain_dir_lst:
        domain_path = os.path.join(domain_dir, "domain_groundtruth.pddl")
        with open(domain_path, "r") as f:
            domain_str = f.read()
        fewshot_domain_model: Domain = DomainParser()(domain_str)
        few_shot_domain_lst.append(fewshot_domain_model)

    llm_input_dict = dict()
    # set context
    llm_input_dict["context"] = (
        PROMPT_CONTEXT
        + PROMPT_OBJECTIVE
        + PROMPT_STYLE
        + PROMPT_TONE
        + PROMPT_AUDIENCE
        + PROMPT_RESPONSE
    )

    # ! set query part 1. few shot examples
    few_shot_str_lst = []
    few_shot_str = """One or two examples from other domains for illustrating the input and output formats.
"""
    for i, fewshot_domain_model in enumerate(few_shot_domain_lst):
        # load the json file
        json_filepath = os.path.join(fewshot_example_domain_dir_lst[i], "cot.json")
        with open(json_filepath, "r") as f:
            cot_response_dict = json.load(f)

        # also get data_info
        fewshot_data_info_module = import_from_filepath(
            os.path.join(fewshot_example_domain_dir_lst[i], "data.py")
        )
        fewshot_domain_nl_desc = fewshot_data_info_module.DOMAIN_DESC
        fewshot_action_name_lst = [
            action.name for action in fewshot_domain_model.actions
        ]
        # get predicate description list
        fewshot_predicate_desc_lst = fewshot_data_info_module.PREDICATE_DESC_LST
        fewshot_predicate_desc_str = "\n".join(
            [
                f"{i+1}. {predicate}"
                for i, predicate in enumerate(fewshot_predicate_desc_lst)
            ]
        )

        # select two actions
        fewshot_two_action_names = random.sample(fewshot_action_name_lst, 2)
        fewshot_two_action_models = [
            action
            for action in fewshot_domain_model.actions
            if action.name in fewshot_two_action_names
        ]

        few_shot_str += f"""Here are two examples from the {fewshot_domain_model.name} domain for demonstrating the output format.
        
Domain information: {fewshot_domain_nl_desc}

A list of available predicates
{fewshot_predicate_desc_str}
"""
        for act_i, fewshot_action_name in enumerate(fewshot_two_action_names):
            few_shot_str += f"Example {act_i+1}"
            few_shot_str += f"""
Action Description: {fewshot_data_info_module.ACTION_DESC_DICT[fewshot_action_name]['detailed']}

Action name: {fewshot_action_name}


Your answer:
---
"""
            # add to few_shot_str_lst
            few_shot_str_lst.append(few_shot_str)
            few_shot_str = ""
            # here comes the answer part
            if if_cot_in_fewshot:

                few_shot_str += f"""{cot_response_dict[fewshot_action_name]}
                
"""
            # add the PDDL action schema
            few_shot_str += f"""**Response:**
{get_action_schema_answer_str(fewshot_two_action_models[act_i], add_hint=True)}
---
"""
            # add to few_shot_str_lst
            few_shot_str_lst.append(few_shot_str)
            few_shot_str = ""
    # ! step 2 the query
    query_str = construct_query_for_modeling(
        domain_nl_desc=domain_nl_desc,
        action_nl_desc=action_nl_desc,
        action_name=action_name,
        predicate_desc_lst=predicate_desc_lst,
    )
    llm_input_dict["fewshot"] = few_shot_str_lst # it contains [example1, answer1, example2, answer2, ...]
    llm_input_dict["query"] = query_str

    return llm_input_dict


# ! MAIN function to get the input dict for the action modeling task
def get_llm_input_dict(
    query_domain_name: str,
    desc_granularity: str,
    if_cot_in_fewshot: bool,
    verbose=False,
):
    """
    Constructs and returns a dictionary mapping action names to LLM input dictionaries.

    Args:
        query_domain_name (str): The name of the domain to query.
        desc_granularity (str): The granularity of the action description.
        if_cot_in_fewshot (bool): Indicates whether to include the context of thought (COT) in the few-shot example.
        verbose (bool, optional): If True, prints additional information for each action. Defaults to False.

    Returns:
        dict: A dictionary mapping action names to LLM input dictionaries.
        dict keys are ['context', 'fewshot', 'query']
    """

    validation_domain_dirs = os.path.join(
        os.environ["WORKING_DIR"], "data/01_raw/pddl_domain/validation_set"
    )
    # pick two domains for few-shot example
    domain_filepaths = glob(
        os.path.join(validation_domain_dirs, f"**/domain_groundtruth.pddl"),
        recursive=True,
    )
    two_domain_filepaths = random.sample(domain_filepaths, 2)
    fewshot_domain_dir_lst = [
        os.path.dirname(domain_filepath) for domain_filepath in two_domain_filepaths
    ]
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

    action_to_query_dict = dict()
    for i, action_name in enumerate(action_name_lst):
        llm_input_dict = construct_llm_input_dict_for_action_modeling(
            domain_nl_desc=query_domain_info.DOMAIN_DESC,
            action_nl_desc=query_domain_info.ACTION_DESC_DICT[action_name][
                desc_granularity
            ],
            action_name=action_name,
            predicate_desc_lst=query_domain_info.PREDICATE_DESC_LST,
            if_cot_in_fewshot=if_cot_in_fewshot,
            fewshot_example_domain_dir_lst=fewshot_domain_dir_lst,
        )
        if verbose:
            print("\n\n\n")
            print(f"Action {i+1}: {action_name}")
            print("\n\n\n")
            print(llm_input_dict["context"])
            print(llm_input_dict["fewshot"])
            print(llm_input_dict["query"])
            print("\n\n\n")

        action_to_query_dict[action_name] = llm_input_dict

    return action_to_query_dict


if __name__ == "__main__":
    query_domain = "doors"
    desc_granularity = "detailed"
    if_cot_in_fewshot = True
    action_to_query_dict = get_llm_input_dict(
        query_domain, desc_granularity, if_cot_in_fewshot, verbose=True
    )
