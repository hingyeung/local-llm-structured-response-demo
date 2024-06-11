# LLM Structured Response

## Structured Response
This repository contains sample code that demonstrates how to guide a Large Language Model (LLM), specifically Llama3, to generate structured responses in a format such as JSON.

The process involves using `PydanticOutputParser` and `RetryOutputParser`. These tools are designed to parse the LLM's responses and convert them into Python classes. This structured format allows for easier manipulation and utilization of the LLM's output in your Python code.

We experiment with two types of prompts in this demonstration: one that includes Llama3's [special tokens](https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3/) and one that does not. Special tokens are specific instructions embedded in the prompts that can guide the LLM to generate responses in a particular format or style. However, in our tests, we found no significant difference in the LLM's responses between the two types of prompts when the special tokens were used correctly. This suggests that the LLM's ability to generate structured responses does not solely depend on the use of special tokens, but also on the overall structure and phrasing of the prompt.


```
task run-structured-response
```

## Function Calling
Large Language Models (LLMs), such as GPT-3 or Llama3, have the ability to generate responses that simulate the behavior of function calls in programming languages. This capability is often referred to as "function calling" within the context of LLMs.

With the experimental `OllamaFunctions` feature from LangChain, we can provide the LLM with a set of "tools". These tools are essentially descriptions of various functions, outlining what they do and how they can be utilized, including the parameters they require.

When a user request is processed, the LLM evaluates whether the provided tools can be used to fulfill the request. If a suitable match is found, the LLM generates a structured `tool_calls` response object. This object details which tools should be used and specifies the parameters to be passed to these tools.

It's important to note that the `tool_calls` response object doesn't execute any functions itself. Instead, it serves as a blueprint that can be used to invoke the actual functions that implement the "tools". This allows us to leverage the pattern recognition capabilities of the LLM to determine the best way to fulfill a user request, while still maintaining control over the actual execution of the functions.

```
run-function-call-response
```