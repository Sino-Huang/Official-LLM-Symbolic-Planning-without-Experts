"""
This is a boilerplate pipeline 'setup_sentence_encoder'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import init_cross_encoder_model



def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=init_cross_encoder_model,
            inputs=['params:setup_sentence_encoder_cfg'],
            outputs="cross_encoder_model",
            name="init_cross_encoder_model_node"
        )
    ])
