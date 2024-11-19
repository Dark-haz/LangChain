# Ensure your VertexAI credentials are configured

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

api_key = os.environ["GOOGLE_API_KEY"]
model = GoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=api_key)

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

completion = model.invoke(messages)

print(completion)