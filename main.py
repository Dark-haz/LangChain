# Ensure your VertexAI credentials are configured

import os
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, trim_messages
from langgraph.graph import START, MessagesState, StateGraph

#_ Model initiation
api_key = os.environ["GOOGLE_API_KEY"]
model = GoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=api_key)

#_ Messages : list of in/out to model 
messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

# completion = model.invoke(messages)
# print(completion)

#_ Prompt template
system_template = "Translate the following from English into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

# result = prompt_template.invoke({"language": "Italian", "text": "hi!"})
# print(result.to_messages())

#_ LangChain Expression Language
chain = prompt_template | model
# response = chain.invoke({"language": "Italian", "text": "hi!"})
# print(response)

#_ Message history
completion = model.invoke(
    [
        HumanMessage(content="Hi! I'm Bob"),
        AIMessage(content="Hello Bob! How can I assist you today?"),
        HumanMessage(content="What's my name?"),
    ]
)

# print(completion)

#_ Message persistance 
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

workflow = StateGraph(state_schema=State)

#_ Advanced prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

#_ Dealing with list of history messages

trimmer = trim_messages( #? messages helper
    max_tokens=50,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

def call_model(state: State):
    chain = prompt | model
    trimmed_messages = trimmer.invoke(state["messages"])
    response = chain.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    return {"messages": [response]}

    
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}


# query = "Hi! I'm Bob."
# input_messages = [HumanMessage(query)]
# output = app.invoke({"messages": input_messages, "language": "Arabic"}, config) # ainvoke for async
# [message.pretty_print() for message in output["messages"]]


# query = "What is my name?"
# input_messages = [HumanMessage(query)]
# output = app.invoke(
#     {"messages": input_messages}, #! can omit language if no changes desired, its persisted
#     config,
# )
# output["messages"][-1].pretty_print()


messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks, i like chocolate ice cream"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

query = "what do i like when it comes to ice cream?"
language = "English"

input_messages = messages + [HumanMessage(query)]
# output = app.invoke(
#     {"messages": input_messages, "language": language},
#     config,
# )
# output["messages"][-1].pretty_print()

#_ Model response streaming
for chunk, metadata in app.stream(
    {"messages": input_messages, "language": language},
    config,
    stream_mode="messages",
):
    if isinstance(chunk, AIMessage):  # Filter to just model responses
        print(chunk.content, end="|")

