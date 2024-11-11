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
    api_key = get_api_token("OPENAI_TOKEN"), 
    model ="gpt-4o",
    has_memory = True, # Enable multi-rounds conversation(with memory)
)

# Tongyi model
# llm = ChatTongyi(
#     api_key = get_api_token("QW_TOKEN"), 
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





