"""
This is a boilerplate pipeline 'post_generate_schema_pool'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import post_generate_schema_pool_parsing


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=post_generate_schema_pool_parsing,
            inputs=[
                "params:post_generate_schema_pool_cfg",
                ],
            outputs=None,
            name="post_generate_schema_pool_parsing_node"
        )
    ])
