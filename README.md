# EasyLangChain

A simplified wrapper around LangChain for easy tool usage.

While LangChain is a powerful framework, I found it over-engineered and highly abstracted, which can make it challenging to use effectively. For example, when implementing LLM + Prompt + Tools + Agents + Memory, I encountered numerous issues where both the official documentation examples and ChatGPT-provided solutions would fail. One specific pain point is the complexity around agent creation - it requires using a separate `create_tool_agents` function and an `AgentExecutor` class (which lacks compatible memory APIs), when a single `Agent` class could potentially handle both responsibilities more elegantly.

However, I do appreciate some of LangChain's standardized design choices, such as the `.invoke` naming convention. I want to use LangChain painlessly. If you've faced similar frustrations, you might want to try this library. EasyLangChain's goal is simple: implement most common functionalities in the simplest way possible.

## Installation

1. from pypi 
```bash
pip install easylangchain
```

2. from github 

```bash
git clone https://github.com/zhiyiZeng/easylangchain.git
cd easylangchain
pip install -r requirements.txt
pip install -e .
```

## A toy example

Example codes are in easylangchain/examples/tryit.py, just run 
```bash 
python tryit.py
```

or copy codes below.

```python 
from easylangchain.llms import ChatTongyi, ChatOpenAI
from easylangchain.tools import tool

weathers = {
    "Beijing": {"2024-11-10": "Sunny", "2024-11-11": "Cloudy"},
    "Shanghai": {"2024-11-10": "Light Rain", "2024-11-11": "Cloudy"},
}


@tool
def get_weather(location: str, date: str = "2024-11-10") -> int:
    """Get the weather of a location on a specific date.
    Args:
        location: The location to get the weather of.
        date: The date to get the weather of. defaults to 2024-11-10.
    """
    print("get_weather is called")
    return weathers[location][date]


# OpenAI model
llm = ChatOpenAI(
    api_key = "YOUR_OPENAI_TOKEN", 
    model ="gpt-4o",
    has_memory = True, # Enable multi-rounds conversation(with memory)
)

# Tongyi model
# llm = ChatTongyi(
#     api_key = "YOUR_QW_TOKEN", 
#     model = "qwen-plus",
#     has_memory = True,
# )

# bind tools
llm.bind_tools([get_weather,])

print("The first round:")
query = "How's the weather in Beijing"
print(f"You: {query}")

# Method 1: Pass a string directly
response = llm.invoke(query)

# Method 2: Pass an OpenAI-style dictionary
# response = llm.invoke({"role": "user", "content": query})

# Method 3: Use LangChain-style message object
# from easylangchain.messages import HumanMessage
# response = llm.invoke(HumanMessage(content=query))

# parse response into string, default format_type is 'str'
print(f"Assistant: {llm.parse_response(response)}")

# The second round
print("\nThe second round:")
response = llm.invoke("What was my last question?")
print(f"Assistant: {llm.parse_response(response)}")

```

As you can see, only minimal abstracts and classes you are exposed to. **All you need to do is to**
- instantiate the model class with `ChatOpenAI()`,
- bind tools if necessary with `.bind()`,
- start your query with `.invoke()`,
- format the result with `.parse_response()`.

In the meanwhile, 
- Don't need to bother what are the differences between `OpenAI` and `ChatOpenAI`.
- Don't need to bother what are the differences between different Message classes, such as `HumanMessage`, `SystemMessage`, `AssistantMessage`, `ToolMessage`...
- Don't need to bother what are the differences between different Memory classes.
- Don't need to bother what are the differences between different Agent classes.
- Don't need to bother what are the differences between different AgentExecutor classes.

With simply wrapping langchain and relevant packages, you can use almost pure python to construct a multi-rounds conversation with tools.



## How about more?

If you want more features, just inherit the base classes of EasyLangChain and rewrite them. It’s easier than you think.

For example, if you want to more output formats, just copy `BaseLLM` from `/easylangchain/llms/models.py` and rewrite `.parse_response()`.

before:

```python 

class BaseLLM

    RESPONSE_FORMAT_TYPES = {
        "str": StrOutputParser(),
    }
    
    ...
    
    def parse_response(self, response, format_type: str = "str"):
        """Parse the response"""
        format_parser = self.RESPONSE_FORMAT_TYPES.get(format_type)
        if format_parser is None:
            raise ValueError("not implemented, you can implement it by updating self.RESPONSE_FORMAT_TYPES using pure python dict grammar.")
        return format_parser.invoke(response)



class ChatOpenAI(BaseLLM):
    ...
```

after:
```python 

class CustomBaseLLM(BaseLLM)
    self.RESPONSE_FORMAT_TYPES = {
        "str": StrOutputParser(),
        "json": JsonOutputParser()
    }
    ...


class ChatOpenAI(CustomBaseLLM):
    ...

```




## Notes 

To be clear, I think langchain is powerful, but I think it's over-engineered. I appreciate langchain commmuity very much😊.




