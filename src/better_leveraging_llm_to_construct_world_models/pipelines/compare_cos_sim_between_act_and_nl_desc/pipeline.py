"""
This is a boilerplate pipeline 'compare_cos_sim_between_act_and_nl_desc'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import analyzing_cos_sim_between_action_and_nl_desc, generate_boxplot_from_cos_sim_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=analyzing_cos_sim_between_action_and_nl_desc,
            inputs=[
                "cross_encoder_model",
                "params:setup_sentence_encoder_cfg",
            ],
            outputs="cosine_sim_comparison_data#csv",
            name="analyzing_cos_sim_between_action_and_nl_desc_node"
        ),
        node(
            func=generate_boxplot_from_cos_sim_data,
            inputs=[
                "cosine_sim_comparison_data#csv"
            ],
            outputs=["boxplot_cosine_sim_comparison#pdf", "boxplot_cosine_sim_with_exp#pdf"],
            name = "generate_boxplot_from_cos_sim_data_node"
        )
    ])
