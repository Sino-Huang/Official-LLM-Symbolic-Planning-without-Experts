
import os, sys, tabulate, csv
from pathlib import Path
import argparse
from subprocess import run
from glob import glob

from better_leveraging_llm_to_construct_world_models.utils.call_planner import call_pddl_planner
import pandas as pd
from better_leveraging_llm_to_construct_world_models.pipelines.bisim_evaluation.merge import main as merge_main


mark = {
    False: '\u274c',
    True: '\u2714'
}

# character for a small red x
# c = '\u274c'

def check_alignment(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id):
    marking_merge_domain_fp = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name, submission_id, "domain.pddl")
    Path(os.path.dirname(marking_merge_domain_fp)).mkdir(parents=True, exist_ok=True)
    problem_basename = os.path.basename(problem_fp)
    marking_merge_problem_fp = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name, submission_id, problem_basename)
    marking_merge_log_fp = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name, submission_id, "merge.log")
    marking_merge_plan_fp = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name,submission_id, "plan.merged")
    marking_merge_planner_log_fp = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name, submission_id, "planner.merged.log")
    
    try: 
        merge_main(domain_groundtruth_fp, problem_fp, generated_domain_fp, problem_fp, marking_merge_domain_fp, marking_merge_problem_fp)
    except Exception as e:
        print(f"Error: {e}")
        with open(marking_merge_log_fp , 'w') as f:
            f.write(str(e))
            
        return ("Diff Parameters", None)
            
  
    
    # solving the merged problem
    
    merge_plan_result = call_pddl_planner(marking_merge_domain_fp, marking_merge_problem_fp)
    if merge_plan_result['is_ok']:
        merge_plan = merge_plan_result['plan_lst']
        logs = merge_plan_result['metrics']
        # save to file
        with open(marking_merge_plan_fp, 'w') as f:
            f.write('\n'.join(merge_plan))
        with open(marking_merge_planner_log_fp, 'w') as f:
            f.write(logs)
    else:
        merge_plan = None
        logs = merge_plan_result['error']
        with open(marking_merge_planner_log_fp, 'w') as f:
            f.write(logs)
    
    # check file for failure message
    with open(marking_merge_planner_log_fp, 'r') as f:
        mtext = f.read()
        align = 'NOTFOUND' in mtext
    if not (align or merge_plan is None):
        print(f'Warning: Alignment failed for {task_domain_name}')

    plan = None
    if os.path.isfile(marking_merge_plan_fp):
        with open(marking_merge_plan_fp, 'r') as f:
            plan = f.read()
    return (align, plan)

def check_solve(task_domain_name, generated_domain_fp, problem_fp):
    
    planner_result = call_pddl_planner(generated_domain_fp, problem_fp)
    if 'plan_lst' not in planner_result:
        return False
    else:
        return True
    

def check_validate(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id, val_path="~/.vscode-server/data/User/globalStorage/jan-dolejsi.pddl/val/Val-20210401.1-Linux/bin/Validate"):
    # the first will check submission_plan_fp (student solution)
    submission_plan_fp = os.path.join(Path(__file__).parent.resolve(), "submission", task_domain_name, submission_id, "plan")
    Path(os.path.dirname(submission_plan_fp)).mkdir(parents=True, exist_ok=True)
    # generate it 
    submission_plan = call_pddl_planner(generated_domain_fp, problem_fp)['plan_lst']
    with open(submission_plan_fp, 'w') as f:
        f.write('\n'.join(submission_plan))
    
    validate_1_log_fp = os.path.join(Path(__file__).parent.resolve(), "marking", task_domain_name,  submission_id, "validate1.log")
    validate_2_log_fp = os.path.join(Path(__file__).parent.resolve(), "marking", task_domain_name, submission_id, "validate2.log")
    Path(os.path.dirname(validate_1_log_fp)).mkdir(parents=True, exist_ok=True)
    
    os.system(f'{val_path} {domain_groundtruth_fp} {problem_fp} {submission_plan_fp} > {validate_1_log_fp} 2>&1')
    with open(validate_1_log_fp, 'r') as f:
        vtext = f.read()
        valid1 = ('Plan executed successfully' in vtext) and ('Plan valid' in vtext)
    
    # the second will check the reference plan (reference solution)
    # the reference plan needs to be generated first 
    reference_plan_fp = os.path.join(Path(__file__).parent.resolve(), "reference", task_domain_name, submission_id, "plan")
    Path(os.path.dirname(reference_plan_fp)).mkdir(parents=True, exist_ok=True)
    # the reference plan needs to be generated first
    reference_plan = call_pddl_planner(domain_groundtruth_fp, problem_fp)['plan_lst']
    with open(reference_plan_fp, 'w') as f:
        f.write('\n'.join(reference_plan))
    
    reference_planner_log_fp = os.path.join(Path(__file__).parent.resolve(), "reference", task_domain_name, submission_id, "planner.log")
    # --- the groundtruth plan should be generated
    reference_plan_result = call_pddl_planner(domain_groundtruth_fp, problem_fp)
    assert 'plan_lst' in reference_plan_result
    reference_plan = reference_plan_result['plan_lst']
    with open(reference_plan_fp, 'w') as f:
        f.write('\n'.join(reference_plan))
    with open(reference_planner_log_fp, 'w') as f:
        f.write(reference_plan_result['metrics'])
    # ---
    
    os.system(f'{val_path} {generated_domain_fp} {problem_fp} {reference_plan_fp} > {validate_2_log_fp} 2>&1')
    with open(validate_2_log_fp, 'r') as f:
        vtext = f.read()
        valid2 = ('Plan executed successfully' in vtext) and ('Plan valid' in vtext)
    return (valid1, valid2)

def format_results(results):
    if list(results.values())[0].get("Domain-Name", None) is not None:
        headers = ['Problem', 'Solve', 'St-Validates', 'Ref-Validates', 'Aligns', "Domain-Name", "Desc-Granularity"]
        rows = []
        for prob in results:
            rows.append([prob, results[prob]['solve'], results[prob]['validates1'], results[prob]['validates2'], results[prob]['aligns'],results[prob]['Domain-Name'], results[prob]['Desc-Granularity']])
            
    else:
        headers = ['Problem', 'Solve', 'St-Validates', 'Ref-Validates', 'Aligns']
        rows = []
        for prob in results:
            rows.append([prob, results[prob]['solve'], results[prob]['validates1'], results[prob]['validates2'], results[prob]['aligns']])
    return tabulate.tabulate(rows, headers=headers, tablefmt='github')

def count_trues(values):
    return len([ v for v in values if mark[True] in v])

def explain_fails(values):
    explanation = ''
    
    for i,v in enumerate(values):
        if mark[False] in v:
            if i == 0:
                explanation += 'Failed to Solve. '
            elif i == 1:
                explanation += 'Failed to validate student solution. '
            elif i == 2:
                explanation += 'Failed to validate reference solution. '
    
    return explanation if len(explanation) > 0 else '-'


def grade(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id):
    print(f"Grading {task_domain_name}...")
    marking_dir_path = os.path.join(Path(__file__).parent.resolve(), "marking", task_domain_name)
    marking_merge_dir_path = os.path.join(Path(__file__).parent.resolve(), "merge", task_domain_name)
    submission_dir_path = os.path.join(Path(__file__).parent.resolve(), "submission", task_domain_name)
    reference_dir_path = os.path.join(Path(__file__).parent.resolve(), "reference", task_domain_name)

    working_dir = os.path.join(Path(__file__).parent.resolve())
    os.chdir(working_dir)
    
    # delete the old marking folder 
    if os.path.exists(marking_dir_path):
        os.system(f'rm -rf {marking_dir_path}')
        os.system(f'rm -rf {marking_merge_dir_path}')
        os.system(f'rm -rf {submission_dir_path}')
        os.system(f'rm -rf {reference_dir_path}')
            
    # mkdir
    Path(marking_dir_path).mkdir(parents=True, exist_ok=True)
    Path(marking_merge_dir_path).mkdir(parents=True, exist_ok=True)
    Path(submission_dir_path).mkdir(parents=True, exist_ok=True)
    Path(reference_dir_path).mkdir(parents=True, exist_ok=True)

    results = {task_domain_name: {}} # the result dictionary contains just a single problem

    # confirm they find plans for all
    print('  finding plans...')
    for prob in results:
        results[prob]['solve'] = mark[check_solve(task_domain_name, generated_domain_fp, problem_fp)] 
    

    # confirm their plans work on our domain
    print('  validating plans...')
    for prob in results:
        if results[prob]['solve'] == mark[True]:
            validates1, validates2 = check_validate(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id) 
            results[prob]['validates1'] = mark[validates1]
            results[prob]['validates2'] = mark[validates2]
        else:
            _, validates2 = check_validate(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id) 
            results[prob]['validates1'] = '-'
            results[prob]['validates2'] = mark[validates2]


    # check the theory alignments
    print('  checking theory alignments...')
    plan_text = ''
    for prob in results:
        align, plan = check_alignment(task_domain_name, domain_groundtruth_fp, generated_domain_fp, problem_fp, submission_id) 
        if plan:
            plan_text += f"\nMis-alignment plan for {prob}:\n{plan}"
        if align == 'Diff Parameters':
            results[prob]['aligns'] = align
        else:
            results[prob]['aligns'] = mark[align]
        
    # format results
    res = format_results(results)

    grade_txt_fp = os.path.join(Path(__file__).parent.resolve(), "marking", task_domain_name,submission_id , "grade.txt")

    with open(grade_txt_fp, 'w', encoding='utf-8') as f:
        f.write(f'\n{res}\n\n{plan_text}\n\n')

    print('Done!\n')
    return results

if __name__ == '__main__':

    domain_name = "libraryworld"
    reference_domain_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/domain_groundtruth.pddl')
    problem_fp = os.path.join(os.environ['WORKING_DIR'], f'data/01_raw/pddl_domain/testing_set/{domain_name}/p0.pddl')
    desc_gran = "detailed"
    
    submission_domain_fp_lst= [
        reference_domain_fp,
        "/home/xxxxxh/Extrastorage/PhDProject_Ext/BetterPDDLModeling/better-leveraging-llm-to-construct-world-models/data/02_intermediate/action_schema_combination/libraryworld_detailed_ensemble_15_use_cp_True_alpha_0.2/domain_model_2990.pddl",
        "/home/xxxxxh/Extrastorage/PhDProject_Ext/BetterPDDLModeling/better-leveraging-llm-to-construct-world-models/data/02_intermediate/action_schema_combination/libraryworld_detailed_ensemble_15_use_cp_True_alpha_0.2/domain_model_2996.pddl"
    ]
    
    # remove the old marking folder
    marking_dir_path = os.path.join(Path(__file__).parent.resolve(), "marking", domain_name)
    marking_merge_dir_path = os.path.join(Path(__file__).parent.resolve(), "merge", domain_name)
    submission_dir_path = os.path.join(Path(__file__).parent.resolve(), "submission", domain_name)
    reference_dir_path = os.path.join(Path(__file__).parent.resolve(), "reference", domain_name)

    working_dir = os.path.join(Path(__file__).parent.resolve())
    os.chdir(working_dir)
    
    # delete the old marking folder 
    if os.path.exists(marking_dir_path):
        os.system(f'rm -rf {marking_dir_path}')
        os.system(f'rm -rf {marking_merge_dir_path}')
        os.system(f'rm -rf {submission_dir_path}')
        os.system(f'rm -rf {reference_dir_path}')
    
    total_results = {}
    for ind, submission_domain_fp in enumerate(submission_domain_fp_lst):
        print(f"-- {ind+1}/{len(submission_domain_fp_lst)} --")
        try:
            res = grade(domain_name, reference_domain_fp, submission_domain_fp, problem_fp, submission_id=str(ind))
            # update name 
            assert len(res) == 1
            new_res = dict()
            for k in res:
                new_res[k+f"_submission_{ind}_{desc_gran}"] = res[k]
                new_res[k+f"_submission_{ind}_{desc_gran}"]['Domain-Name'] = k
                new_res[k+f"_submission_{ind}_{desc_gran}"]['Desc-Granularity'] = desc_gran
            res = new_res
        except Exception as e:
            print(f"Error: {e}")
            continue
        # update result 
        total_results.update(res)
    # format results
    res = format_results(total_results)
    # write to file
    grade_txt_fp = os.path.join(os.path.join(os.path.dirname(__file__)), "marking", "all_grade.txt")
    # create the parent dir 
    Path(os.path.dirname(grade_txt_fp)).mkdir(parents=True, exist_ok=True)
    # need to add explanation for each column
    exp_str = """Explanation:
Solve: This term is used to assess whether the planner can find a plan based on the generated domain model.
St-Validates: This term is used to assess whether the plan generated from the domain model is valid when applied to the actual groundtruth domain setting.
Ref-Validates: This term is used to evaluate whether the reference solution (groundtruth plan) is valid when applied to the generated domain model.
Aligns: This term is used to assess the equivalence between two planning domains are “equivalent” using Bisimulation theory."""
    with open(grade_txt_fp, 'w', encoding='utf-8') as f:
        f.write(f'\n{exp_str}\n\n')
        f.write(f'#\n{res}\n\n')
        
    # also convert to dataframe and save to csv
    df  = pd.DataFrame(total_results)
    df.to_csv(grade_txt_fp.replace('.txt', '.csv'))
    print('Done!\n')
