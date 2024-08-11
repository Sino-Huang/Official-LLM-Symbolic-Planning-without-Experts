"""
This is a boilerplate pipeline 'action_schema_combination'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node 
from .nodes import action_schema_combi

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=action_schema_combi,
            inputs=[
                "params:general",
                "params:setup_sentence_encoder_cfg",
                "params:finetuning_encoder_cfg",
                "params:action_schema_combination_cfg",
                "cp_threshold#json",
            ],
            outputs="action_combi_analysis#csv",
            name="action_schema_combi_node"
        ),
    ])
