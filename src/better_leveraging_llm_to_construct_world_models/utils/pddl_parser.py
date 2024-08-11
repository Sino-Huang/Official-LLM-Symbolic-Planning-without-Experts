from pddl.parser.domain import DomainParser
from pddl.parser.problem import ProblemParser
from pddl.formatter import domain_to_string, problem_to_string
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect
import os 
from glob import glob

def get_domain_model_from_name(domain_name):
    data_dir_path = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain')
    domain_file_pattern = os.path.join(data_dir_path, f"**/{domain_name}/domain_groundtruth.pddl")
    domain_filepaths = glob(domain_file_pattern, recursive=True)
    domain_names = [os.path.basename(os.path.dirname(domain_filepath)) for domain_filepath in domain_filepaths]
    if domain_name not in domain_names:
        raise ValueError(f"Domain {domain_name} does not exist in the data directory.")
    domain_filepath = domain_filepaths[domain_names.index(domain_name)]
    with open(domain_filepath, 'r') as f:
        domain_str = f.read()
    domain_model = DomainParser()(domain_str)
    return domain_model

def get_action_schema_answer_str(action: Action, add_hint=False):
    output = f"""Parameters:
{get_beautiful_parameter_str(action, add_hint=add_hint)}

Preconditions:
```
{get_beautiful_precondition_str(action)}
```

Effects:
```
{get_beautiful_effect_str(action)}
```
"""
    return output

def get_domain_action_schema(data):
    if isinstance(data, str):
        domain_model = DomainParser()(data)
        action_schema = domain_model.actions 
    elif isinstance(data, Domain):
        action_schema = data.actions
    else:
        raise ValueError(f"Invalid data type: {type(data)}")
    
    return action_schema


def get_beautiful_parameter_str(action: Action, add_hint=False):
    parameter_str_lst = [] 
    for param in action.parameters:
        if isinstance(param, Constant):
            term_str =  f"{param.name} - {param.type.name}"
        elif isinstance(param, Variable):
            tag_type_str = " ".join(list(param.type_tags))
            if len(list(param.type_tags)) > 1:
                tag_type_str = "(either " + tag_type_str + ")"
            term_str = f"?{param.name} - {tag_type_str}"
            
        if add_hint:
            term_str += f": [short description of the parameter]"
        parameter_str_lst.append(term_str)
        
    parameter_str = "\n".join([f"{i+1}. {term}" for i, term in enumerate(parameter_str_lst)])
    return parameter_str

def get_beautiful_precondition_str(action: Action):
    # add 4 indentations
    output_str = ""
    if isinstance(action.precondition, And):
        output_str += "(and\n"
        for term in action.precondition.operands:
            output_str += f"    {term}\n"
        output_str += ")"
    else:
        output_str = str(action.precondition)
    return output_str

def get_beautiful_effect_str(action: Action):
    # add 4 indentations
    output_str = ""
    if isinstance(action.effect, AndEffect):
        output_str += "(and\n"
        for term in action.effect.operands:
            output_str += f"    {term}\n"
        output_str += ")"
    else:
        output_str = str(action.effect)
        
    return output_str


