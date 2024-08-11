"""
This is a boilerplate pipeline 'tree_of_thought_direct_planning'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import query_plans_llm


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=query_plans_llm,
            inputs=["params:general", "params:tot_direct_planning_cfg"],
            outputs=None,
            name="query_plans_lln_node"
        )
    ])
