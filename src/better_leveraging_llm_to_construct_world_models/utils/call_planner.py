import os
import re
import time
from glob import glob
from typing import List, Dict, Sequence, Union
import requests
from urllib.parse import urlparse
from icecream import ic


def call_pddl_planner(
    domain_fp_str,
    problem_fp_str,
    solver_url="http://localhost:5001/package/dual-bfws-ffparser/solve",  # ! this solver url often changes, default: https://solver.planning.domains/solve  local: http://localhost:5001/package/dual-bfws-ffparser/solve , http://localhost:5001/package/lama-first/solve
    waiting_sec=1.05,
    waiting_interval=0.1,
    verbose=False,
):
    """
    Calls an online planner to solve a planning problem.

    Args:
        domain_fp_str (str): File path to the domain file or domain model str.
        problem_fp_str (str): File path to the problem file or domain model str.
        solver_url (str, optional): URL of the online planner solver. Defaults to "http://solver.planning.domains/solve".

    Returns:
        dict: A dictionary containing the result of the planning process.
            - is_ok (bool): Indicates whether the planning process was successful.
            - plan_lst (list): List of actions in the plan.
            - metrics (str): Metrics and logs from the planning process.
            - error (str): Error message if the planning process encountered an error.
    """
    linux_path_regex = r"^(/[^/ ]*)+/?$"
    windows_path_regex = r"^[A-Z]:(\\[^\\]+)+\\?$"

    # check if domain_fp and problem_fp are file paths or domain model str
    if bool(re.match(linux_path_regex, domain_fp_str)) or bool(
        re.match(windows_path_regex, domain_fp_str)
    ):
        with open(domain_fp_str, "r") as f:
            domain_data = f.read()
    else:
        domain_data = domain_fp_str

    if bool(re.match(linux_path_regex, problem_fp_str)) or bool(
        re.match(windows_path_regex, problem_fp_str)
    ):
        with open(problem_fp_str, "r") as f:
            problem_data = f.read()
    else:
        problem_data = problem_fp_str

    data = {  # lower case the domain and problem data
        "domain": domain_data.lower(),
        "problem": problem_data.lower(),
    }
    response = requests.post(solver_url, verify=False, json=data)
    try:
        response_json = response.json()
    except Exception as e:
        print("Error in Finding PDDL Plan")
        print("Solver URL:")
        print(solver_url)
        print("Response Content:")
        print(response.content)
        time.sleep(10)
        return call_pddl_planner(domain_fp_str, problem_fp_str, solver_url, waiting_sec, waiting_interval, verbose)
        # raise e

    if "status" not in response_json and "result" in response_json:
        # need to continue to get the result
        newurl = response_json["result"]
        parsed_uri = urlparse(solver_url)
        solver_url_host = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
        new_solver_info_url = solver_url_host + "/" + newurl
        pending_count = 0
        while pending_count < waiting_sec:
            response = requests.get(new_solver_info_url, verify=False)
            response_json = response.json()
            if "status" not in response_json or response_json["status"] == "PENDING":
                time.sleep(waiting_interval)
                pending_count += waiting_interval
                continue
            else:
                break

        if pending_count >= waiting_sec:  # timeout
            error_message = "Valid Syntax but Timeout in Getting the Plan"
            return {"is_ok": False, "error": error_message}

    if verbose:
        print(response_json)
    # return response_json # ! debug use
    # ! the json format may changes
    if response_json is None or "status" not in response_json:
        print("Machine get no response, try to sleep 10s and try again")
        time.sleep(10)
        return call_pddl_planner(domain_fp_str, problem_fp_str, solver_url, waiting_sec, waiting_interval, verbose)
        
    if response_json["status"] == "error":
        print("Found Error")
        # error_message = response_json['result']['error']
        error_message = response_json["result"]["stderr"]
        return {"is_ok": False, "error": error_message}
    elif response_json["status"] == "ok":
        # plan = [act['name'] for act in response_json['result']['plan']]
        try:
            raw_plan = response_json["result"]["output"]["plan"]
        except KeyError as e:
            print("Error in Finding PDDL Plan")
            print("Response Content:")
            print(response_json["result"])
            time.sleep(10)
            return call_pddl_planner(domain_fp_str, problem_fp_str, solver_url, waiting_sec, waiting_interval, verbose)
            # return {"is_ok": False, "error": str(e)}
            
        bad_output_flag = False
        if raw_plan == "":
            bad_output_flag = True

        if response_json["result"]["stderr"] != "":
            bad_output_flag = True
        if not bad_output_flag:
            plan = response_json["result"]["output"]["plan"].split("\n")
            plan = [p.lower() for p in plan if p != ""]

            # metricslogs = response_json['result']['output']
            metricslogs = (
                response_json["result"]["stderr"]
                + "\n"
                + response_json["result"]["stdout"]
            )

            # if want to save to a file, use f.write('\n'.join(list))

            return {"is_ok": True, "plan_lst": plan, "metrics": metricslogs}
        else:
            error_message = (
                response_json["result"]["stderr"]
                + "\n"
                + response_json["result"]["stdout"]
            )
            return {"is_ok": False, "error": error_message}


if __name__ == "__main__":
    pddl_data_dir = os.path.join(os.environ['WORKING_DIR'], 'data/01_raw/pddl_domain')
    domain_pattern = os.path.join(pddl_data_dir, '**/domain_groundtruth.pddl')
    
    domain_filepaths= glob(domain_pattern, recursive=True)
    for domain_filepath in domain_filepaths:
        # get parent directory
        parent_dir = os.path.dirname(domain_filepath)
        problem_filepaths = glob(os.path.join(parent_dir, 'p*.pddl'))
        
        for problem_filepath in problem_filepaths:
            print(f"Domain: {domain_filepath}")
            print(f"Problem: {problem_filepath}")
            # result = call_pddl_planner(domain_filepath, problem_filepath, solver_url="http://192.168.20.129:5001/package/dual-bfws-ffparser/solve")
            result = call_pddl_planner(domain_filepath, problem_filepath)
            if result['is_ok']:
                print("Plan:")
                print(result['plan_lst'])
            else:
                print("Error:")
                print(result['error'])
            print()
            time.sleep(0.1)