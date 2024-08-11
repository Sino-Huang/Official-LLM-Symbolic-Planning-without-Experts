"""
This is a boilerplate pipeline 'finetuning_sentence_encoder'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import train_sentence_encoder, generate_plot_from_finetuned_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_sentence_encoder,
            inputs=[
                "params:setup_sentence_encoder_cfg",
                "params:finetuning_encoder_cfg",
                "cosine_sim_comparison_data#csv",
                ],
            outputs=["validation_set_cosine_sim_comparison_data_after_finetune#csv", "testing_set_cosine_sim_comparison_data_after_finetune#csv"],
            name="train_sentence_encoder_node"
        ),
        node(
            func=generate_plot_from_finetuned_model,
            inputs=["validation_set_cosine_sim_comparison_data_after_finetune#csv", "testing_set_cosine_sim_comparison_data_after_finetune#csv"],
            outputs=["validation_set_cosine_sim_comparison_after_finetune#pdf",
                     "testing_set_cosine_sim_comparison_after_finetune#pdf"],
            name="generate_plot_from_finetuned_model_node",
        )
    ])
