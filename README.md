# EasyLangChain

A simplified wrapper around LangChain for easy tool usage.

While LangChain is a powerful framework, I found it over-engineered and highly abstracted, which can make it challenging to use effectively. For example, when implementing LLM + Prompt + Tools + Agents + Memory, I encountered numerous issues where both the official documentation examples and ChatGPT-provided solutions would fail. One specific pain point is the complexity around agent creation - it requires using a separate `create_tool_agents` function and an `AgentExecutor` class (which lacks compatible memory APIs), when a single `Agent` class could potentially handle both responsibilities more elegantly.

However, I do appreciate some of LangChain's standardized design choices, such as the `.invoke` naming convention. I want to use LangChain painlessly. If you've faced similar frustrations, you might want to try this library. EasyLangChain's goal is simple: implement most common functionalities in the simplest way possible.

## Installation

```python
git clone https://github.com/zhiyiZeng/easylangchain.git
cd easylangchain
pip install -e .
```

## Requirements
