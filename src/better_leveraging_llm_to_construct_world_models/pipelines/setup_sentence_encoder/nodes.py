"""
This is a boilerplate pipeline 'setup_sentence_encoder'
generated using Kedro 0.19.6
"""
# ref: https://sbert.net/docs/pretrained-models/msmarco-v3.html
# ref: https://sbert.net/docs/sentence_transformer/pretrained_models.html#semantic-search-models
# ref: https://sbert.net/docs/pretrained-models/ce-msmarco.html

# model : cross-encoder/ms-marco-MiniLM-L-12-v2

from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers import SentenceTransformer
from better_leveraging_llm_to_construct_world_models.prompt_template.main_prompting_template import get_llm_input_dict
from better_leveraging_llm_to_construct_world_models.utils.pddl_parser import get_action_schema_answer_str, get_domain_model_from_name
from icecream import ic

def create_sentence_encoder_helper(setup_sentence_encoder_cfg):
    model_name = setup_sentence_encoder_cfg['model_name']
    model_type = setup_sentence_encoder_cfg['model_type']
    device = setup_sentence_encoder_cfg['device']
    if model_type == "cross_encoder":
        model = CrossEncoder(model_name)
    elif model_type == "bi_encoder":
        model = SentenceTransformer(model_name)
        
    return model

# ! NODE
def init_cross_encoder_model(setup_sentence_encoder_cfg):
    model_type = setup_sentence_encoder_cfg['model_type']
    is_evaluated = setup_sentence_encoder_cfg['is_evaluated']
    model = create_sentence_encoder_helper(setup_sentence_encoder_cfg)
    
    if not is_evaluated:
        # we run some test
        query_domain = "doors"
        desc_granularity = "detailed"
        if_cot_in_fewshot = True
        action_to_query_dict = get_llm_input_dict(query_domain, desc_granularity, if_cot_in_fewshot)
        doors_domain_model = get_domain_model_from_name(query_domain)
        action_names = list(action_to_query_dict.keys())
        action_model_list = list(doors_domain_model.actions)
        target_action = action_names[0]
        target_action_query_str = action_to_query_dict[target_action]['context'] + action_to_query_dict[target_action]['query'] # in prelim test we found that it is important to include context
        
        testing_action_answer_lst = []
        testing_action_lst = []
        for action_model in action_model_list:
            testing_action_answer = get_action_schema_answer_str(action_model)
            testing_action_answer_lst.append(testing_action_answer)
            testing_action_lst.append(action_model.name)
            
        # we run the model
        print("Target action:", target_action)
        print("Testing Action List:", testing_action_lst)
        if model_type == "cross_encoder":
            ranks = model.rank(target_action_query_str, testing_action_answer_lst)
            for rank in ranks:
                print(rank['score'], '\t', rank['corpus_id'], '\t', rank.keys())
        elif model_type == "bi_encoder":
            # cross encoder is compatible for the following code
            query_embedding = model.encode(target_action_query_str, convert_to_tensor=True)
            corpus_embeddings = model.encode(testing_action_answer_lst, convert_to_tensor=True)
            similarity_scores = model.similarity(query_embedding, corpus_embeddings)
            print(similarity_scores)
        ic(model.similarity_fn_name)
        
    
    return model


