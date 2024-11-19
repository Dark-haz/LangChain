import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
import os

print("start")
os.environ["GOOGLE_API_KEY"] = getpass.getpass()

from langchain_google_vertexai import ChatVertexAI

model = ChatVertexAI(model="gemini-1.5-flash" , project="451307300202" )

from langchain_core.messages import HumanMessage

m = model.invoke([HumanMessage(content="Hi! I'm Bob")])
print(m)
# model.invoke([HumanMessage(content="What's my name?")])