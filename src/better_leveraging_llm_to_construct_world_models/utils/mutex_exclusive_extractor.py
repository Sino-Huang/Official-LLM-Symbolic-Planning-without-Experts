import re
from copy import deepcopy
import numpy as np
from pddl.logic import Predicate, Constant, Variable
from pddl.logic.base import And, Not, Or, BinaryOp, UnaryOp
from pddl.core import Domain, Problem, Action, Requirements, Formula
from pddl.logic.effects import AndEffect
import os 
from subprocess import run
from pddl.parser.domain import DomainParser
import itertools
from natsort import natsorted


def extract_variable_values(sas):
    output_dict = dict() # {var_id: [var_values]}
    lines = sas.split("\n")
    for i, line in enumerate(lines):
        if line == "begin_variable":
            var_id = lines[i+1]
            var_id = re.search(r"\d+", var_id).group(0)
            val_size = int(lines[i+3])
            var_values = []
            for j in range(val_size):
                value = lines[i+4+j]
                if "NegatedAtom" in value:
                    value = value.replace("NegatedAtom ", "not (")
                    value += ")"
                elif "Atom" in value:
                    value = value.replace("Atom ", "")
                    
                var_values.append(value)
                
            output_dict[var_id] = var_values
            
    return output_dict

def extract_mutex_groups(sas, var_dict):
    output_dict = dict() # {mutex_id: [mutex_groups]}
    lines = sas.split("\n")
    count = len(var_dict)
    for i, line in enumerate(lines):
        if line == "begin_mutex_group":
            val_size = int(lines[i+1])
            mutex_group = []
            for j in range(val_size):
                var_id, var_val_id = lines[i+2+j].split(" ")
                var_id = str(var_id)
                var_val_id = int(var_val_id)
                value = var_dict[var_id][var_val_id]
                mutex_group.append(value)
            output_dict[str(count)] = mutex_group
            count += 1
    return output_dict
            
def obtain_obj_mutex_dict(sas):
    var_dict = extract_variable_values(sas)
    mutex_dict = extract_mutex_groups(sas, var_dict)
    output_dict = dict()
    output_dict.update(var_dict)
    output_dict.update(mutex_dict)
    return output_dict

def obtain_translated_mutex_info(domain_file, problem_file, fast_downward_path):
    CWD = os.getcwd()
    run([fast_downward_path, "--translate", domain_file, problem_file])
    # get the output file
    output_file = os.path.join(CWD, "output.sas")
    with open(output_file, "r") as f:
        sas = f.read()
    # remove the output file
    os.remove(output_file)
    return obtain_obj_mutex_dict(sas)

def reformat_pred_expression(item):
    limit = 10
    count = 0 
    while count < limit:
        match = re.search(r'(\w+)(\([^\(\)]*\))', item)
        match2 = re.search(r'not\s\((.*\))', item)
        if match is None and match2 is None:
            break
        else:
            if match is not None:
                end_stuffs = match.group(2)[1:] + item[match.end(2):]
                if len(end_stuffs) > 1:
                    offset = " "
                else:
                    offset = ""
                item = item[:match.start(1)] + '(' + match.group(1) + offset + end_stuffs
                count += 1
            elif match2 is not None:
                item = "(not " + match2.group(1)
                count += 1
                break
    return item
            
    
def find_all_occurrences(pattern, text):
    """Finds all occurrences of a pattern in a string and returns their start and end indices.

    Args:
        pattern: The regular expression pattern to search for.
        text: The string to search within.

    Returns:
        A list of tuples, where each tuple contains the start and end index of a match.
    """
    matches_inds = []
    match_names = []
    for match in re.finditer(pattern, text):
        matches_inds.append((match.start(1), match.end(1)))
        match_names.append(match.group(1))
    return matches_inds, match_names


def get_mutex_var_version(mutex_dict, var_lst):
    variables = set()
    vari_location_dict = dict()
    for key, value in mutex_dict.items():
        vari_location_dict[key] = dict()
        for var_val_ind, item in enumerate(value):
            # Find all lowercase letters within parentheses
            matches_inds, match_names = find_all_occurrences(r'[\s(]([a-z])[,)]+', item)
            if len(matches_inds) > 0:
                for i, match in enumerate(matches_inds):
                    obj_name = match_names[i]
                    if var_val_ind not in vari_location_dict[key]:
                        vari_location_dict[key][var_val_ind] = dict()
                    if obj_name not in vari_location_dict[key][var_val_ind]:
                        vari_location_dict[key][var_val_ind][obj_name] = []
                    vari_location_dict[key][var_val_ind][obj_name].append(match)
                    variables.add(obj_name)
    
            
    # map the variable names to the original variable names
    # consider combinations 
    all_combi = []
    for permu in itertools.permutations(variables, len(var_lst)):
        combi = {a:b for a, b in list(zip(permu, var_lst))}
        all_combi.append(combi)
        
    output_mapping_data = [] 
    
    for combi_k_var_v_obj_dict in all_combi:
        for key, value in mutex_dict.items():
            output_lst = [] 
            for var_val_ind, item in enumerate(value):
                if var_val_ind not in vari_location_dict[key]:
                    output_lst.append(item)
                    continue
                obj_name_match_dict = vari_location_dict[key][var_val_ind] # {obj_name: [(start, end)]}
                obj_name_set_in_raw = set(obj_name_match_dict.keys())
                obj_name_set_in_combi = set(combi_k_var_v_obj_dict.keys())
                if obj_name_set_in_raw - obj_name_set_in_combi != set():
                    continue
                else:
                    updated_item = ""
                    do_not_add_inds = [] 
                    for i in range(len(item)):
                        if i in do_not_add_inds:
                            continue
                        swap_flag = False 
                        for obj_name_r in obj_name_match_dict:
                            for match in obj_name_match_dict[obj_name_r]:
                                start, end = match
                                if i == start:
                                    # update do not add inds
                                    do_not_add_inds += list(range(start, end))
                                    # check variable name
                                    var_name = combi_k_var_v_obj_dict[obj_name_r]
                                    updated_item += f"?{var_name}"
                                    swap_flag = True
                                    break
                            if swap_flag:
                                break
                        if not swap_flag:
                            updated_item += item[i]
                            
                    if updated_item != "":
                        output_lst.append(updated_item)
                                    
            if len(output_lst) > 0:
                output_mapping_data.append(output_lst)
        
    unique_output_mapping_data = []
    for item in output_mapping_data:
        sort_item = natsorted(item)
        if sort_item not in unique_output_mapping_data:
            unique_output_mapping_data.append(sort_item)
    # reformat the output
    for i, item in enumerate(unique_output_mapping_data):
        for j, sub_item in enumerate(item):
            unique_output_mapping_data[i][j] = reformat_pred_expression(sub_item)
    return unique_output_mapping_data


def get_manipulated_mutex_exclusive_predicate(action_model: Action, mutex_obj_dict):
    # get effect 
    effect = action_model.effect
    # get all the predicates in the effect
    if isinstance(effect, AndEffect):
        predicates = list(effect.operands)
    else:
        predicates = [effect]
        
    # get str ver
    predicates_str = [str(pred) for pred in predicates]
    params = action_model.parameters
    params_name_lst = [param.name for param in params]
    mutex_var_version_lst = get_mutex_var_version(mutex_obj_dict, params_name_lst)
    mutex_output = []
    
    for pred_str in predicates_str:
        for mutex_var_version in mutex_var_version_lst:
            if pred_str in mutex_var_version:
                # get ind of pred_str
                ind = mutex_var_version.index(pred_str)
                for i, item in enumerate(mutex_var_version):
                    if i == ind:
                        continue
                    mutex_output.append(item)
    return mutex_output        


if __name__ == "__main__":
    example_sas = """begin_version
3
end_version
begin_metric
0
end_metric
7
begin_variable
var0
-1
4
Atom holding(c)
Atom on(c, a)
Atom on(c, b)
Atom ontable(c)
end_variable
begin_variable
var1
-1
2
Atom clear(c)
NegatedAtom clear(c)
end_variable
begin_variable
var2
-1
2
Atom clear(a)
NegatedAtom clear(a)
end_variable
begin_variable
var3
-1
2
Atom clear(b)
NegatedAtom clear(b)
end_variable
begin_variable
var4
-1
2
Atom handempty()
NegatedAtom handempty()
end_variable
begin_variable
var5
-1
4
Atom holding(a)
Atom on(a, b)
Atom on(a, c)
Atom ontable(a)
end_variable
begin_variable
var6
-1
4
Atom holding(b)
Atom on(b, a)
Atom on(b, c)
Atom ontable(b)
end_variable
4
begin_mutex_group
4
2 0
5 0
6 1
0 1
end_mutex_group
begin_mutex_group
4
3 0
5 1
6 0
0 2
end_mutex_group
begin_mutex_group
4
1 0
5 2
6 2
0 0
end_mutex_group
begin_mutex_group
4
4 0
5 0
6 0
0 0
end_mutex_group
begin_state
3
1
0
0
0
2
3
end_state
begin_goal
2
5 1
6 2
end_goal
18
begin_operator
pick-up a
0
3
0 2 0 1
0 4 0 1
0 5 3 0
1
end_operator
begin_operator
pick-up b
0
3
0 3 0 1
0 4 0 1
0 6 3 0
1
end_operator
begin_operator
pick-up c
0
3
0 1 0 1
0 4 0 1
0 0 3 0
1
end_operator
begin_operator
put-down a
0
3
0 2 -1 0
0 4 -1 0
0 5 0 3
1
end_operator
begin_operator
put-down b
0
3
0 3 -1 0
0 4 -1 0
0 6 0 3
1
end_operator
begin_operator
put-down c
0
3
0 1 -1 0
0 4 -1 0
0 0 0 3
1
end_operator
begin_operator
stack a b
0
4
0 2 -1 0
0 3 0 1
0 4 -1 0
0 5 0 1
1
end_operator
begin_operator
stack a c
0
4
0 2 -1 0
0 1 0 1
0 4 -1 0
0 5 0 2
1
end_operator
begin_operator
stack b a
0
4
0 2 0 1
0 3 -1 0
0 4 -1 0
0 6 0 1
1
end_operator
begin_operator
stack b c
0
4
0 3 -1 0
0 1 0 1
0 4 -1 0
0 6 0 2
1
end_operator
begin_operator
stack c a
0
4
0 2 0 1
0 1 -1 0
0 4 -1 0
0 0 0 1
1
end_operator
begin_operator
stack c b
0
4
0 3 0 1
0 1 -1 0
0 4 -1 0
0 0 0 2
1
end_operator
begin_operator
unstack a b
0
4
0 2 0 1
0 3 -1 0
0 4 0 1
0 5 1 0
1
end_operator
begin_operator
unstack a c
0
4
0 2 0 1
0 1 -1 0
0 4 0 1
0 5 2 0
1
end_operator
begin_operator
unstack b a
0
4
0 2 -1 0
0 3 0 1
0 4 0 1
0 6 1 0
1
end_operator
begin_operator
unstack b c
0
4
0 3 0 1
0 1 -1 0
0 4 0 1
0 6 2 0
1
end_operator
begin_operator
unstack c a
0
4
0 2 -1 0
0 1 0 1
0 4 0 1
0 0 1 0
1
end_operator
begin_operator
unstack c b
0
4
0 3 -1 0
0 1 0 1
0 4 0 1
0 0 2 0
1
end_operator
0
"""
    test_domain =  "./test_domain.pddl"
    test_domain = os.path.join(os.path.dirname(__file__), test_domain)
    with open(test_domain, 'r') as f:
        test_domain = f.read()
    test_action = list(DomainParser()(test_domain).actions)[0]
    obj_mutex_dict = obtain_obj_mutex_dict(example_sas)
    mutex_output = get_manipulated_mutex_exclusive_predicate(test_action, obj_mutex_dict)
    print(mutex_output)
    