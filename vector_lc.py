import os
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


#_ Document : chunks of larger document 
documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = Chroma.from_documents(
    documents,
    embedding=embeddings,
)

similarity = vectorstore.similarity_search("cat")
# vectorstore.similarity_search_with_score("cat")
# vectorstore.similarity_search_by_vector(embedding)
# print(similarity)

#_ Retriever --> runnables , can use vector store to use them in chains

retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
# retriever = vectorstore.as_retriever(    search_type="similarity",search_kwargs={"k": 1},)

# similarity  = retriever.batch(["cat", "shark"])
# print(similarity)

#_ Simple RAG using retriever runnable
#TODO check out what are runnables and where are they used

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

api_key = os.environ["GOOGLE_API_KEY"]
model = GoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=api_key)

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model

response = rag_chain.invoke("tell me about cats")

print(response)