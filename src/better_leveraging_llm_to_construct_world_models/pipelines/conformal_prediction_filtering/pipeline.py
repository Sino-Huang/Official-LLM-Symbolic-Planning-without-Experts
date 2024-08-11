"""
This is a boilerplate pipeline 'conformal_prediction_filtering'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import calculate_cp_threshold

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=calculate_cp_threshold,
            inputs=[
                "params:setup_sentence_encoder_cfg",
                "params:finetuning_encoder_cfg",
                "params:conformal_prediction_filtering_cfg",
                "cosine_sim_comparison_data#csv",
                ],
            outputs="cp_threshold#json",
            name="calculate_cp_threshold_node"
        )
    ])
