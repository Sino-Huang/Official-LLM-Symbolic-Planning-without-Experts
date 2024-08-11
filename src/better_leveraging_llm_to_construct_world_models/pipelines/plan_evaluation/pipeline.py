"""
This is a boilerplate pipeline 'plan_evaluation'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import human_plan_eval


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=human_plan_eval,
            inputs=["params:plan_evaluation_cfg"],
            outputs="human_evaluation_results#csv",
            name="human_plan_eval_node"
        )
    ])
