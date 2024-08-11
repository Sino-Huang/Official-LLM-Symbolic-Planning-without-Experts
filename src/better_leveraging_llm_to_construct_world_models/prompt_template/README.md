## Structure of the LLM Input

```python
dict{
    k=action_name: {
        "context": str,
        "fewshot": str,
        "query": str,
    }
}
```

- context (str): The context, also known as system prompt
- fewshot (str): The fewshot learning examples
- query (str): The query, also known as user prompt