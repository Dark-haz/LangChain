
import os
from google.auth import compute_engine
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI


PROJECT_ID = "fir-test-ee6a3"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

client = firestore.Client(
    project=PROJECT_ID
)

history = FirestoreChatMessageHistory(
    session_id=SESSION_ID, collection=COLLECTION_NAME, client=client
)

api_key = os.environ["GOOGLE_API_KEY"]

model= ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

while True:
    prompt = input()
    history.add_user_message(prompt)

    ai_response = model.invoke(history.messages)
    history.add_ai_message(ai_response.content)

    print(ai_response)