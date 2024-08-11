from .main_prompting_template import PROMPT_RESPONSE
# this can be used for gathering CoT few shot examples 

COT_CONTEXT_FOR_EXPLANATION = """# CONTEXT #
You are a tool called PDDL Modeling Assistant. \
You are a technical experts in explaining why the natural language context results in the corresponding domain model.
"""

COT_OBJECTIVE_FOR_EXPLANATION = """# OBJECTIVE #
* Explain in simple, natural language why the why the the user's natural language description leads to the current action schema.
* Focus on the motivation why the preconditions are necessary and how they lead to the specified effects. Use a scenario to illustrate the explanation.
* Describe why the preconditions are necessary and how they lead to the specified effects.
* Use straightforward, easy-to-understand language so that even someone without technical expertise, like my grandma, can understand.
"""

COT_STYLE_FOR_EXPLANATION = """# STYLE #
Follow the style of a teacher explaining a concept to a student. Use simple language and avoid jargon.
"""

COT_TONE_FOR_EXPLANATION = """# TONE #
Be patient and kind. Explain the concept as if you were teaching it to a child.
"""

COT_AUDIENCE_FOR_EXPLANATION = """# AUDIENCE #
Your audience is someone who is not familiar with the technical details of PDDL.
"""

COT_RESPONSE_FOR_EXPLANATION = """# RESPONSE #
The response should be in the following format:
---
**Explanation:** [Your explanation here]
---
"""

def construct_query_for_explanation(domain_nl_desc, action_nl_desc, action_name, predicate_desc_lst, pddl_action_schema):
    
    # add line number to each predicate description and join them using \n
    predicate_desc_str = "\n".join([f"{i+1}. {predicate}" for i, predicate in enumerate(predicate_desc_lst)])
    
    output = f"""Question: Here is the natural language descriptions.
A natural language description of the domain
Domain information: {domain_nl_desc}
A natural language description of the action
Action: {action_nl_desc}
The name of the action
Action name: {action_name}
A list of available predicates
{predicate_desc_str}

Here is the corresponding PDDL action schema.
{pddl_action_schema}

Your answer:
"""
    return output
    
    
    
if __name__ == "__main__":
    query_str = construct_query_for_explanation("domain_nl_desc", "action_nl_desc", "action_name", ["predicate 1: explanation", "predicate 2: explain blah blah"], PROMPT_RESPONSE)
    print(query_str)