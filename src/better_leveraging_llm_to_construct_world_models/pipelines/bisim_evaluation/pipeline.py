"""
This is a boilerplate pipeline 'bisim_evaluation'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import bisim_evaluate


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=bisim_evaluate,
            inputs=["params:bisim_evaluation_cfg"],
            outputs="bisim_evaluation_results#csv",
            name="bisim_evaluate_node"
        )
    ])
