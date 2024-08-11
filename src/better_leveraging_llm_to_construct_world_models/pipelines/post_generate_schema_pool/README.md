## Use
This pipeline will try to post-process the output of the LLM response into structured PDDL domain files. We will use PDDL parser from https://github.com/jan-dolejsi/vscode-pddl to fix syntax errors. 

After getting all the domains, we will again use pddl DomainParser to parse the domain and if the domain is not valid, we use vscode-pddl to fix the syntax errors.

## Note
The use of LLMs to iteratively fix syntax errors using parser feedback is proven to be effective in many existing work but this method is extremely expensive. A simple alternative is to use a PDDL parser to fix syntax errors. Our work focuses on the semantic (factual) errors in the LLM output, thus we will not spend budget on using LLMs to fix syntax errors.

## After getting candidates 
we will do the combination generate a group of domain model candidates with confidence score being the accumulated cosine similarity of the semantic validator. 