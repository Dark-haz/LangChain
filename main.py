# Ensure your VertexAI credentials are configured

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


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

print(completion)