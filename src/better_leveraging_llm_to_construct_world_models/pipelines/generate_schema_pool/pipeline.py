"""
This is a boilerplate pipeline 'generate_schema_pool'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import query_llm
from pathlib import Path

from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
import os 

def create_pipeline(**kwargs) -> Pipeline:
    
    return pipeline([
        node(
            func=query_llm,
            inputs=[
                "params:general",
                "params:generate_schema_pool_cfg",
                ],
            outputs=None,
            name="query_llm_node"
        )
    ])
