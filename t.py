from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage , HumanMessage, SystemMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

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
   
]
ai_msg = llm.invoke(messages)

print(ai_msg.content)