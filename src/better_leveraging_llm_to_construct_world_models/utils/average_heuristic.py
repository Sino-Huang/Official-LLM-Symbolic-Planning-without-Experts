from glob import glob 

import os 

import json 
from tqdm.auto import tqdm 


if __name__ == "__main__":
    dirpath = "/home/xxxxxh/Extrastorage/PhDProject_Ext/BetterPDDLModeling/better-leveraging-llm-to-construct-world-models/data/07_model_output/tree_of_thought_plans"
    
    file_pattern = os.path.join(dirpath, "**/summary_for_problem_*.jsonl")
    
    file_lst = glob(file_pattern, recursive=True)
    
    for filepath in tqdm(file_lst):
        data = [] 
        
        with open(filepath, "r") as f:
            for line in f:
                data.append(json.loads(line))
                
        # for each data, we get heuristic val and divide by the length of plan
        for d in data:
            d["heuristic"] = round(d["heuristic"] / len(d["plan"]), 2)
            
        # sort the data by heuristic value descending
        data = sorted(data, key=lambda x: x["heuristic"], reverse=True)
        
        # write back to file
        with open(filepath, "w") as f:
            for d in data:
                f.write(json.dumps(d) + "\n")
                
        