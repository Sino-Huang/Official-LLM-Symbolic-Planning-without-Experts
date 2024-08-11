"""
This is a boilerplate pipeline 'post_construction_ranking'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import generate_plans_with_scores


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=generate_plans_with_scores,
            inputs=[
                "params:general",
                "params:setup_sentence_encoder_cfg",
                "params:finetuning_encoder_cfg",
                "params:post_construction_ranking_cfg"
            ],
            outputs=None,
            name="generate_plans_with_scores_node"
        )
    ])
