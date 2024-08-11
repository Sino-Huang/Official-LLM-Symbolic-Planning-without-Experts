#!/bin/bash

export PYTHONPATH=$PWD

# kedro run --from-nodes=init_cross_encoder_model_node --to-nodes=generate_boxplot_from_cos_sim_data_node --params setup_sentence_encoder_cfg.model_type=bi_encoder

# ! only redraw the boxplot
kedro run --from-nodes=generate_boxplot_from_cos_sim_data_node -p compare_cos_sim_between_act_and_nl_desc