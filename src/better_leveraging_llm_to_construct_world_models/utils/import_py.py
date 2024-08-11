import importlib.util
import sys
import os 
from glob import glob

def import_from_filepath(filepath):
    module_name = filepath.split('/')[-1].split('.')[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module