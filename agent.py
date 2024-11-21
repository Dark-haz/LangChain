# Import relevant functionality
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_google_genai import GoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Create the agent
api_key = os.environ["GOOGLE_API_KEY"]
from langchain_google_genai import ChatGoogleGenerativeAI

model= ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

#_ Tool
search = TavilySearchResults(max_results=2 , description="Search engine can be used to search for relevant real time answers when you dont have the exact answer including getting the current weather ")

# search_results = search.invoke("what is the weather in SF")
# print(search_results)

#_ Model with tool equipped
tools = [search]
model_with_tools = model.bind_tools(tools)

# response = model_with_tools.invoke([HumanMessage(content="whats the weather in SF")])
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

#_ Agent , binds model with tools
agent_executor = create_react_agent(model, tools)
response = agent_executor.invoke(
    {"messages": [HumanMessage(content="whats the weather in sf?")]}
)
# [message.pretty_print() for message in response["messages"]]

#_ Memory
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}


# # Use the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config 
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
):
    print(chunk)
    print("----")